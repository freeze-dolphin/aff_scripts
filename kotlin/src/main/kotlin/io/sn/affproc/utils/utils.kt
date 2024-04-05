package io.sn.affproc.utils

import com.tairitsu.compose.arcaea.*

fun genTrace(timing: Long, endTiming: Long, startPosition: Position, endPosition: Position): ArcNote {
    return ArcNote(timing, endTiming, startPosition.toPair(), ArcNote.Type.S, endPosition.toPair(), ArcNote.Color.BLUE, true) {}
}

fun genAnimationTrace(timing: Long, startPosition: Position, endPosition: Position): ArcNote {
    return genTrace(timing, timing, startPosition, endPosition)
}

fun Difficulty.quickArctap(time: Number, position: Position): Note {
    return arcNote(time.toLong() - 1, time.toLong(), position.toPair(), this.s, position.toPair()) {
        arctap(time.toInt())
    }
}