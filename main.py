import numpy as num
import matplotlib.pyplot as mpl

#setting up simulation to run for 30s in 0.1s steps
stepTime = 0.1
totalTime = 30.0
numberOfSteps = int(totalTime / stepTime)

speed = 0.5
speedNoise = 0.03
turningRate = 0.2
turningNoise = 0.02
rand = num.random.default_rng(42)

x = 0.0 
y = 0.0 
orientation = 0.0

#xPositions = [x]
#yPositions = [y]

trueXPosition = [x]
trueYPosition = [y]

estimatedX = 0.0
estimatedY = 0.0 
estimatedOrientation = 0.0
estimatedXPosition = [estimatedX]
estimatedYPosition = [estimatedY]

for i in range(numberOfSteps):
    orientation = orientation + turningRate * stepTime

    x = x + speed * num.cos(orientation) * stepTime
    y = y + speed * num.sin(orientation) * stepTime

    #xPositions.append(x)
    #yPositions.append(y)
    trueXPosition.append(x)
    trueYPosition.append(y)

    measuredSpeed = speed + rand.normal(0, speedNoise)
    measuredTurningRate = turningRate + rand.normal(0, turningNoise)

    estimatedOrientation += measuredTurningRate * stepTime
    estimatedX += measuredSpeed * num.cos(estimatedOrientation) * stepTime
    estimatedY += measuredSpeed * num.sin(estimatedOrientation) * stepTime
    estimatedXPosition.append(estimatedX)
    estimatedYPosition.append(estimatedY)

xErrors = num.array(estimatedXPosition) - num.array(trueXPosition)
yErrors = num.array(estimatedYPosition) - num.array(trueYPosition)

positionError = num.sqrt(xErrors**2 + yErrors**2)
finalError = positionError[-1]
positionRMSE = num.sqrt(num.mean(positionError**2))

print("Final position error:", round(finalError, 2), "metres")
print("position RMSE:", round(positionRMSE, 2), "metres")

mpl.plot(trueXPosition, trueYPosition, label="Robot Path")
mpl.plot(estimatedXPosition, estimatedYPosition, label="Estimated Path")
mpl.scatter(trueXPosition[0], trueYPosition[0], label="Start")
mpl.scatter(trueXPosition[-1], trueYPosition[-1], label="Finish")

mpl.xlabel("x position (metres)")
mpl.ylabel("y position (metres)")
mpl.title("Robot Movement Simulation")
mpl.legend()
mpl.grid(True)
mpl.axis("equal")
mpl.savefig("trajectory_comparison.png", dpi=300)
mpl.show()