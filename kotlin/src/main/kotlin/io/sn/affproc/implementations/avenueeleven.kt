package io.sn.affproc.implementations

import com.tairitsu.compose.arcaea.ArcNote
import com.tairitsu.compose.arcaea.Position
import com.tairitsu.compose.arcaea.toPosition
import io.sn.affproc.utils.*
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sqrt
import kotlin.random.Random

val avenueElevenNoteTeleportGetFrame = fun(
    hideTiming: Long,
    _: Double,
    position: Position,
    progress: Double,
    _: Long,
    duration: Any?,
): List<ArcNote> {
    val offset = easeOutCubic(progress) * duration as Long / 2

    return listOf(ArcNote(
        (hideTiming + offset - 1).toLong(),
        (hideTiming + offset).toLong(),
        position.toPair(),
        ArcNote.Type.S,
        position.toPair(),
        ArcNote.Color.BLUE,
        true
    ) {
        arctap((hideTiming + offset).toInt())
    })

}

val avenueElevenNoteJumpGetFrame = fun(
    hideTiming: Long,
    duration: Double,
    position: Position,
    progress: Double,
    extraNoteOffset: Long,
    extra: Any?,
): List<ArcNote> {
    val targetPosition = extra!! as Position
    val currentCoord = getParabolaCoordinateAtTime(NoteInfo(position.x, 0.0), NoteInfo(targetPosition.x, duration), progress)
    val offset = (currentCoord.second * ARCAEA_COORD_SYSTEM_ZOOM_CONSTANT + extraNoteOffset).toLong()

    println(offset)

    return listOf(ArcNote((hideTiming + offset - 1), (hideTiming + offset), currentCoord.toPosition().apply {
        y = 0.0
    }, ArcNote.Type.S, currentCoord.toPosition().apply {
        y = 0.0
    }, ArcNote.Color.BLUE, true
    ) {
        arctap((hideTiming + offset).toInt())
    })
}

var ARCAEA_COORD_SYSTEM_ZOOM_CONSTANT = 2000

private data class NoteInfo(var xInArcCoordSystem: Double, val distanceBetweenNoteAndJudge: Double) {
    val x: Long = (xInArcCoordSystem * ARCAEA_COORD_SYSTEM_ZOOM_CONSTANT).toLong()
    val y: Long = distanceBetweenNoteAndJudge.toLong()

}

/**
 * 返回结果中的 Point, x 为 arc 中的横坐标值, y 为距离判定平面的距离
 */
private fun getParabolaCoordinateAtTime(a: NoteInfo, b: NoteInfo, progress: Double): Pair<Double, Double> {
    val g = 9.81 // 重力加速度
    val t = sqrt(2 * (b.y - a.y) / g) // 计算运动总时间

    // 根据抛物线的方程 x = v0x * t 和 y = a.y + v0y * t - 0.5 * g * t^2 计算位置
    val x = a.x + (b.x - a.x) * progress
    val y = a.y + (b.y - a.y) * progress - 0.5 * g * t * t * progress * progress

    return Pair(x / ARCAEA_COORD_SYSTEM_ZOOM_CONSTANT, y)
}

fun genCollapseTraceGroup(
    startTiming: Long,
    endTiming: Long,
    startPos: Position,
    endPos: Position,
    segmentNum: Int,
    easingFunction: EasingFunction,
    amplifier: Double,
    amplitude: Double,
): List<ArcNote> {
    val result = mutableListOf<ArcNote>()

    var resizedAmplifier = Random.nextDouble(-amplitude, amplitude) + amplifier

    val cuttingSeq = getRandomSeq(startTiming, endTiming, segmentNum)
    cuttingSeq.add(0, startTiming)
    cuttingSeq.add(endTiming)

    var curPos = startPos
    var curEndPos = balancePos(startPos, endPos, curPos, 1.0 / segmentNum, easingFunction, resizedAmplifier)

    for (idx in (0..segmentNum)) {
        val progress = (idx + 1).toDouble() / segmentNum
        resizedAmplifier = Random.nextDouble(-amplitude, amplitude) + amplifier
        result.add(
            ArcNote(
                cuttingSeq[idx] + if (Random.nextDouble() < 0.2) 0 else Random.nextInt(
                    max(((cuttingSeq[idx + 1] - cuttingSeq[idx]) / 2).toInt(), 1) * -1,
                    max(((cuttingSeq[idx + 1] - cuttingSeq[idx]) / 2).toInt(), 1) * 1
                ),
                cuttingSeq[idx + 1],
                curPos,
                ArcNote.Type.S,
                curEndPos,
                ArcNote.Color.BLUE,
                true
            )
        )
        val tmpPos =
            curPos.copy().offsetWith(Random.nextDouble(amplifier / -2, amplifier / 2), Random.nextDouble(amplifier / -2, amplifier / 2))
        curPos = curEndPos.copy()
        curEndPos = balancePos(startPos, endPos, tmpPos, progress, easingFunction, resizedAmplifier)
    }

    return result
}

private fun balancePos(
    startPos: Position,
    endPos: Position,
    curPos: Position,
    progress: Double,
    easingFunction: EasingFunction,
    amplifier: Double,
): Position {
    val easedPos = easePos(startPos, endPos, easingFunction, progress)

    return curPos.apply {
        val sgnY = (easedPos.y > curPos.y).let {
            if (it) 1 else -1
        }
        val sgnX = (easedPos.x > curPos.x).let {
            if (it) 1 else -1
        }


        y = max(
            0.0,

            y + sgnY * 2 * abs(easedPos.y - curPos.y)
                    + Random.nextDouble(-amplifier / 2, amplifier / 2)

        )
        x = min(
            1.5, max(
                -0.5,

                x + sgnX * 2 * abs(easedPos.x - curPos.x)
                        + Random.nextDouble(-amplifier * 3, amplifier * 3)

            )
        )
    }
}

private fun getRandomSeq(startTiming: Long, endTiming: Long, segmentNum: Int): MutableList<Long> {
    val cuttingPoints = mutableListOf<Long>()
    repeat(segmentNum) {
        var rand: Long
        do {
            rand = Random.nextLong(startTiming + 1, endTiming)
        } while (cuttingPoints.contains(rand))
        cuttingPoints.add(rand)
    }
    cuttingPoints.sort()
    return cuttingPoints
}
