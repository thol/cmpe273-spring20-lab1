import os
import datetime
import asyncio

sortedFinal = []
async def splitList(inputList):
    listLen = len(inputList)
    mid = listLen // 2
    return inputList[:mid], inputList[mid:]

async def mergeList(leftList, rightList):
    if len(leftList) == 0:
        return rightList
    elif len(rightList) == 0:
        return leftList

    leftIndex = 0
    rightIndex = 0
    listMerged = []
    lenTargetList = len(leftList) + len(rightList)
    while len(listMerged) < lenTargetList:
        if (leftList[leftIndex] <= rightList[rightIndex]):
            listMerged.append(leftList[leftIndex])
            leftIndex += 1
        else:
            listMerged.append(rightList[rightIndex])
            rightIndex += 1

        if rightIndex == len(rightList):
            listMerged += leftList[leftIndex:]
            break
        elif leftIndex == len(leftList):
            listMerged += rightList[rightIndex:]
            break
        
    return listMerged

def mergeSort(numList):
    if len(numList) <= 1:
        return numList
    else:
        left, right = splitList(numList)
        sortedLeft = mergeSort(left)
        sortedRight = mergeSort(right)
        return mergeList(sortedLeft, sortedRight)
    

def getSortedListFromFile(numFile):
    with open(numFile) as f:
        lineList = [int(numValue.rstrip()) for numValue in f.readlines()]
    return mergeSort(lineList)

async def writeSortedFile(fileName, sortedList):
    with open(fileName,'w') as out:
        out.writelines("%d\n" % num for num in sortedList)

async def processFile(unsortedFile):
    sortedFile = unsortedFile.replace("input/unsorted","output/sorted")
    sortedList = getSortedListFromFile(unsortedFile)
    await writeSortedFile(sortedFile,sortedList)
    sortedFinal.append(sortedList)

async def main ():
    startTime = datetime.datetime.now()
    dirname = os.path.dirname(__file__)
    input_path = os.path.join(dirname,'input')
    # coroutines = list()
    # loop = asyncio.get_event_loop()
    for file in os.listdir(input_path):
        unsortedFile = input_path + "/" + file
        await asyncio.gather(processFile(unsortedFile))
        # loop.run_until_complete(task)
        # coroutines.append()
        # await asyncio.gather(processFile(unsortedFile))   
    # await asyncio.gather(*coroutines)
    

    finalOutput = os.path.join(dirname,'output','sorted.txt')
    writeSortedFile(finalOutput,mergeSort(sortedFinal))
    endTime = datetime.datetime.now()

    duration = endTime - startTime
    print("Duration {0} seconds and {1} ms".format(duration.total_seconds(),duration.microseconds))

if __name__ == '__main__':
    asyncio.run(main())
