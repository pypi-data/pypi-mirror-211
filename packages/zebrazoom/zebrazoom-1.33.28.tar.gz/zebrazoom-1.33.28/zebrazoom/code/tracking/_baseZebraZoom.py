import math
import pickle
import os
import cv2

import numpy as np

from zebrazoom.code.dataPostProcessing.dataPostProcessing import dataPostProcessing

from ._base import BaseTrackingMethod
from ._getBackground import GetBackgroundMixin


class BaseZebraZoomTrackingMethod(BaseTrackingMethod, GetBackgroundMixin):
  '''Base class for tracking implementations which use ZebraZoom mixins.'''

  def _debugFrame(self, frame, title=None, buttons=(), timeout=None):
    raise ValueError("debug mode is not available without the GUI")

  def dataPostProcessing(self, outputFolder, superStruct):
    # Various post-processing options depending on configuration file choices
    return dataPostProcessing(outputFolder, superStruct, self._hyperparameters, *os.path.splitext(os.path.basename(self._videoPath)))

  def _debugTracking(self, frameNumber: int, output: list, outputHeading: list, frame2: np.array) -> None:
    pass

  def _updateBackgroundAtInterval(self, i, wellNumber, initialCurFrame, trackingHeadTailAllAnimals, frame):
    if i % self._hyperparameters["updateBackgroundAtInterval"] == 0:
      showImages = False
      firstFrameToShow = 10
      if showImages and i > firstFrameToShow:
        self._debugFrame(self._background, title='background before')
      xvalues = [trackingHeadTailAllAnimals[0, i-self._firstFrame][k][0] for k in range(0, len(trackingHeadTailAllAnimals[0, i-self._firstFrame]))]
      yvalues = [trackingHeadTailAllAnimals[0, i-self._firstFrame][k][1] for k in range(0, len(trackingHeadTailAllAnimals[0, i-self._firstFrame]))]
      xmin = min(xvalues)
      xmax = max(xvalues)
      ymin = min(yvalues)
      ymax = max(yvalues)
      dist = 1 * math.sqrt((xmax - xmin) ** 2 + (ymax - ymin) ** 2)
      xmin = int(xmin - dist) if xmin - dist >= 0 else 0
      xmax = int(xmax + dist) if xmax + dist < len(frame[0]) else len(frame[0]) - 1
      ymin = int(ymin - dist) if ymin - dist >= 0 else 0
      ymax = int(ymax + dist) if ymax + dist < len(frame) else len(frame) - 1
      if xmin != xmax and ymin != ymax:
        partOfBackgroundToSave = self._background[self._wellPositions[wellNumber]["topLeftY"]+ymin:self._wellPositions[wellNumber]["topLeftY"]+ymax, self._wellPositions[wellNumber]["topLeftX"]+xmin:self._wellPositions[wellNumber]["topLeftX"]+xmax].copy() # copy ???
        if showImages and i > firstFrameToShow:
          self._debugFrame(partOfBackgroundToSave, title='partOfBackgroundToSave')
      self._background[self._wellPositions[wellNumber]["topLeftY"]:self._wellPositions[wellNumber]["topLeftY"]+self._wellPositions[wellNumber]["lengthY"], self._wellPositions[wellNumber]["topLeftX"]:self._wellPositions[wellNumber]["topLeftX"]+self._wellPositions[wellNumber]["lengthX"]] = initialCurFrame.copy()
      if showImages and i > firstFrameToShow:
        self._debugFrame(self._background, title='background middle')
      if xmin != xmax and ymin != ymax:
        self._background[self._wellPositions[wellNumber]["topLeftY"]+ymin:self._wellPositions[wellNumber]["topLeftY"]+ymax, self._wellPositions[wellNumber]["topLeftX"]+xmin:self._wellPositions[wellNumber]["topLeftX"]+xmax] = partOfBackgroundToSave
      if showImages and i > firstFrameToShow:
        self._debugFrame(self._background, title='background after')

  @staticmethod
  def __rollingMedianFilter(array, window):
    array2 = np.convolve(array, np.ones(window), 'same') / window
    array2[:window-1] = array[:window-1]
    array2[-window+1:] = array[-window+1:]
    return array2

  def _postProcessMultipleTrajectories(self, trackingHeadTailAllAnimals, trackingProbabilityOfGoodDetection):
    maxDistanceAuthorized = self._hyperparameters["postProcessMaxDistanceAuthorized"]
    maxDisapearanceFrames = self._hyperparameters["postProcessMaxDisapearanceFrames"]

    # Removing all points for which the sum of all pixels of the inverted image (the "probability of good detection") is too low
    if self._hyperparameters["postProcessRemoveLowProbabilityDetection"]:
      for animalId in range(0, len(trackingHeadTailAllAnimals)):
        probabilityOfGoodDetection = trackingProbabilityOfGoodDetection[animalId, :]
        if self._hyperparameters["postProcessLowProbabilityDetectionPercentOfMaximum"] == 0:
          toRemove   = (probabilityOfGoodDetection - np.mean(probabilityOfGoodDetection) < -self._hyperparameters["postProcessLowProbabilityDetectionThreshold"] * np.std(probabilityOfGoodDetection))
        else:
          toRemove   = (probabilityOfGoodDetection < np.max(probabilityOfGoodDetection) * self._hyperparameters["postProcessLowProbabilityDetectionPercentOfMaximum"])
        print("Well ", animalId, ": Number of elements to remove:", np.sum(toRemove), " out of ", len(toRemove), "elements")
        trackingHeadTailAllAnimals[animalId, toRemove, 0, 0] = 0
        trackingHeadTailAllAnimals[animalId, toRemove, 0, 1] = 0

    # Removing all points that are too close to the borders
    if self._hyperparameters["postProcessRemovePointsOnBordersMargin"]:
      borderMargin = self._hyperparameters["postProcessRemovePointsOnBordersMargin"]
      for animalId in range(0, len(trackingHeadTailAllAnimals)):
        for frameNumber in range(0, len(trackingHeadTailAllAnimals[animalId])):
          xHead = trackingHeadTailAllAnimals[animalId][frameNumber][0][0]
          yHead = trackingHeadTailAllAnimals[animalId][frameNumber][0][1]
          if (xHead <= borderMargin) or (yHead <= borderMargin) or (xHead >= self._wellPositions[animalId]["lengthX"] - borderMargin - 1) or (yHead >= self._wellPositions[animalId]["lengthY"] - borderMargin - 1):
            trackingHeadTailAllAnimals[animalId][frameNumber][0][0] = 0
            trackingHeadTailAllAnimals[animalId][frameNumber][0][1] = 0

    # Removing all points that are deviating too much from the main trajectory
    if self._hyperparameters["postProcessRemovePointsAwayFromMainTrajectory"]:
      for animalId in range(0, len(trackingHeadTailAllAnimals)):
        xHeadPositions = trackingHeadTailAllAnimals[animalId, :, 0, 0]
        yHeadPositions = trackingHeadTailAllAnimals[animalId, :, 0, 1]
        xHeadPositionsRollingMedian = self.__rollingMedianFilter(xHeadPositions, 11)
        yHeadPositionsRollingMedian = self.__rollingMedianFilter(yHeadPositions, 11)
        distance = np.sqrt((xHeadPositions - xHeadPositionsRollingMedian) ** 2 + (yHeadPositions - yHeadPositionsRollingMedian) ** 2)
        distanceRollingMedian = self.__rollingMedianFilter(distance, 5)
        normalizedDistance = np.array([1 for x in range(0,len(xHeadPositions))])
        normalizedDistance = distance / distanceRollingMedian
        normalizedDistance = np.nan_to_num(normalizedDistance, nan=1)
        toRemove   = normalizedDistance - np.mean(normalizedDistance) > self._hyperparameters["postProcessRemovePointsAwayFromMainTrajectoryThreshold"] * np.std(normalizedDistance)
        trackingHeadTailAllAnimals[animalId, toRemove, 0, 0] = 0
        trackingHeadTailAllAnimals[animalId, toRemove, 0, 1] = 0

    currentlyZero  = False
    zeroFrameStart = 0
    for animalId in range(0, len(trackingHeadTailAllAnimals)):
      for frameNumber in range(0, len(trackingHeadTailAllAnimals[animalId])):
        xHead = trackingHeadTailAllAnimals[animalId][frameNumber][0][0]
        yHead = trackingHeadTailAllAnimals[animalId][frameNumber][0][1]
        if frameNumber != 0:
          xHeadPrev = trackingHeadTailAllAnimals[animalId][frameNumber-1][0][0]
          yHeadPrev = trackingHeadTailAllAnimals[animalId][frameNumber-1][0][1]
        else:
          xHeadPrev = trackingHeadTailAllAnimals[animalId][frameNumber][0][0]
          yHeadPrev = trackingHeadTailAllAnimals[animalId][frameNumber][0][1]
        if ((xHead == 0 and yHead == 0) or (math.sqrt((xHead - xHeadPrev)**2 + (yHead - yHeadPrev)**2) > maxDistanceAuthorized)) and (frameNumber != len(trackingHeadTailAllAnimals[animalId]) - 1):
          if not(currentlyZero):
            zeroFrameStart = frameNumber
          # print("currentlyZero at True: animalId:", animalId, "; frameNumber:", frameNumber)
          currentlyZero = True
        else:
          if currentlyZero:
            if zeroFrameStart >= 1:
              xHeadStart = trackingHeadTailAllAnimals[animalId][zeroFrameStart-1][0][0]
              yHeadStart = trackingHeadTailAllAnimals[animalId][zeroFrameStart-1][0][1]
            else:
              xHeadStart = trackingHeadTailAllAnimals[animalId][frameNumber][0][0]
              yHeadStart = trackingHeadTailAllAnimals[animalId][frameNumber][0][1]
            xHeadEnd = trackingHeadTailAllAnimals[animalId][frameNumber][0][0]
            yHeadEnd = trackingHeadTailAllAnimals[animalId][frameNumber][0][1]
            if (math.sqrt((xHeadEnd - xHeadStart)**2 + (yHeadEnd - yHeadStart)**2) < maxDistanceAuthorized) or (frameNumber - zeroFrameStart > maxDisapearanceFrames):
              currentlyZero = False
              if (math.sqrt((xHeadEnd - xHeadStart)**2 + (yHeadEnd - yHeadStart)**2) < maxDistanceAuthorized) and not((xHeadEnd == 0) and (yHeadEnd == 0)):
                xStep = (xHeadEnd - xHeadStart) / (frameNumber - zeroFrameStart)
                yStep = (yHeadEnd - yHeadStart) / (frameNumber - zeroFrameStart)
                for frameAtZeroToChange in range(zeroFrameStart, frameNumber):
                  trackingHeadTailAllAnimals[animalId][frameAtZeroToChange][0][0] = xHeadStart + xStep * (frameAtZeroToChange - zeroFrameStart)
                  trackingHeadTailAllAnimals[animalId][frameAtZeroToChange][0][1] = yHeadStart + yStep * (frameAtZeroToChange - zeroFrameStart)
              else:
                for frameAtZeroToChange in range(zeroFrameStart, frameNumber):
                  trackingHeadTailAllAnimals[animalId][frameAtZeroToChange][0][0] = xHeadStart
                  trackingHeadTailAllAnimals[animalId][frameAtZeroToChange][0][1] = yHeadStart

  @staticmethod
  def _calculateAngle(xStart, yStart, xEnd, yEnd):
    vx = xEnd - xStart
    vy = yEnd - yStart
    if vx == 0:
      if vy > 0:
        lastFirstTheta = math.pi/2
      else:
        lastFirstTheta = (3*math.pi)/2
    else:
      lastFirstTheta = np.arctan(abs(vy/vx))
      if (vx < 0) and (vy >= 0):
        lastFirstTheta = math.pi - lastFirstTheta
      elif (vx < 0) and (vy <= 0):
        lastFirstTheta = lastFirstTheta + math.pi
      elif (vx > 0) and (vy <= 0):
        lastFirstTheta = 2*math.pi - lastFirstTheta
    return lastFirstTheta

  @staticmethod
  def _distBetweenThetas(theta1, theta2):
    diff = 0
    if theta1 > theta2:
      diff = theta1 - theta2
    else:
      diff = theta2 - theta1
    if diff > math.pi:
      diff = (2 * math.pi) - diff
    return diff

  @staticmethod
  def _assignValueIfBetweenRange(value, minn, maxx):
    if value < minn:
      return minn
    if value > maxx:
      return maxx
    return value

  def getBackground(self):
    outputFolderVideo = os.path.join(self._hyperparameters["outputFolder"], self._videoName)
    if self._hyperparameters["backgroundSubtractorKNN"] or (self._hyperparameters["headEmbeded"] and self._hyperparameters["headEmbededRemoveBack"] == 0 and self._hyperparameters["headEmbededAutoSet_BackgroundExtractionOption"] == 0 and self._hyperparameters["adjustHeadEmbededTracking"] == 0) or self._hyperparameters["trackingDL"] or self._hyperparameters["fishTailTrackingDifficultBackground"]:
      background = []
    else:
      print("start get background")
      if self._hyperparameters["reloadBackground"]:
        outfile = open(os.path.join(outputFolderVideo, 'intermediaryBackground.txt'),'rb')
        background = pickle.load(outfile)
        print("Background Reloaded")
      else:
        outfile = open(os.path.join(outputFolderVideo, 'intermediaryBackground.txt'),'wb')
        background = self._getBackground()
        pickle.dump(background, outfile)
        cv2.imwrite(os.path.join(outputFolderVideo, 'background.png'), background)
      outfile.close()

    if self._hyperparameters["exitAfterBackgroundExtraction"]:
      print("exitAfterBackgroundExtraction")
      raise ValueError

    return background
