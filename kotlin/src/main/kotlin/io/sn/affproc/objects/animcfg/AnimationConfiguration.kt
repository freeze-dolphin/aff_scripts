package io.sn.affproc.objects.animcfg

import com.tairitsu.compose.arcaea.ArcNote
import com.tairitsu.compose.arcaea.Position
import io.sn.affproc.utils.EasingFunction

data class AnimationConfiguration(
    val basicCfg: AnimationBasicConfigurtion,
    val startTiming: Long,
    val duration: Long,
    val radius: Triple<Double, Double, EasingFunction>,
    val position: Triple<Position, Position, EasingFunction>,
    val extraNoteOffset: Long,
    val generateArcNotes: (Long, Double, Position, Double, Long, Any?) -> List<ArcNote>,
    val extra: Any?,
)
