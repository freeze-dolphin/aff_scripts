package io.sn.affproc

import java.io.File
import com.tairitsu.compose.arcaea.*
import io.sn.affproc.objects.AnimationBasicConfigurtion
import io.sn.affproc.utils.addAnimation
import io.sn.affproc.utils.linear
import io.sn.affproc.implementations.ddddddGetFrame
import io.sn.affproc.utils.easeOutCubic
import io.sn.affproc.utils.pos

fun main() {
    mapSet {
        difficulties.future {
            timing(
                offset = -20,
                bpm = 88,
                beats = 999,
            )

            val animBasicCfg = AnimationBasicConfigurtion(120, bpm.toDouble(), 146389 + 1)

            addAnimation(
                animBasicCfg,
                0,
                5434,
                Triple(0.0, 1.0, easeOutCubic),
                Triple(0.0 pos 0.0, 0.0 pos 0.0, linear),
                100L,
                ddddddGetFrame,
                null
            )
        }
    }.writeToFolder(File(File("."), "result"))
}
