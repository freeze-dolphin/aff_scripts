package io.sn.affproc.implementations

import com.tairitsu.compose.arcaea.*
import io.sn.affproc.objects.animcfg.AnimationBasicConfigurtion
import io.sn.affproc.utils.*
import java.io.File
import kotlin.test.Test

class AvenueElevenExec {

    @Test
    fun noteTeleport() {
        mapSet {
            difficulties.future {
                chart.audioOffset = -660
                timing(
                    offset = 0,
                    bpm = 126,
                    beats = 4,
                )

                val globalOffset = 260279L

                if (false) {
                    holdNote(17140, 18807, 4)
                    arcNote(17140, 19045, 0.0 to 1.0, si, 1.0 to 1.0) {
                        arctap(17140)
                    }
                    arcNote(17140, 18569, 0 to 1, siso, 0.5 to 0) {
                        arctap(18569)
                    }
                    arcNote(17140, 18093, 0 to 1, siso, 0.25 to 0.25) {
                        arctap(18093)
                    }
                    arcNote(17140, 17616, 0 to 1, siso, 0 to 0.5) {
                        arctap(17616)
                    }

                    holdNote(19045, 20712, 1)
                }

                val animBasicCfg = AnimationBasicConfigurtion(120, bpm.toDouble(), globalOffset + 1)

                listOf(17378, 17497, 17854, 18330, 18806, 19045).let {
                    it.dropLast(1).forEachIndexed { index, time ->
                        addAnimation(
                            animBasicCfg,
                            time.toLong(),
                            it[index + 1] - time.toLong(),
                            Triple(1.0, 1.0, linear),
                            Triple(1.0 pos 1.0, 1.0 pos 1.0, linear),
                            1,
                            avenueElevenNoteTeleportGetFrame,
                            it[index + 1] - time.toLong()
                        )
                    }
                }

                timingGroup {
                    timing(19045, 99999, 4)
                    quickArctap(19045, 1.0 pos 1.0)
                }

                listOf(19282, 19401, 19759, 20235, 20712).let {
                    it.dropLast(1).forEachIndexed { index, time ->
                        addAnimation(
                            animBasicCfg,
                            time.toLong(),
                            it[index + 1] - time.toLong(),
                            Triple(1.0, 1.0, linear),
                            Triple(0.0 pos 1.0, 0.0 pos 1.0, linear),
                            1,
                            avenueElevenNoteTeleportGetFrame,
                            it[index + 1] - time.toLong()
                        )
                    }
                }

                timingGroup {
                    timing(20712, 99999, 4)
                    quickArctap(20712, 0.0 pos 1.0)
                }
            }
        }.writeToFolder(File(File("."), "result"))
    }

    @Test
    fun noteJump() {
        mapSet {
            difficulties.beyond {
                chart.audioOffset = -660
                timing(
                    offset = 0,
                    bpm = 126,
                    beats = 4,
                )

                val globalOffset = 260279L

                val animBasicCfg = AnimationBasicConfigurtion(120, bpm.toDouble(), globalOffset + 1)

                /*
                - jump from 89047 (-0.50,0.00) to 89523 (1.50,0.00)
                - jump from 89285 (-0.50,0.00) to 89523 (-0.50,0.00)
                 */

                addAnimation(
                    animBasicCfg,
                    89047,
                    89523 - 89047,
                    Triple(1.0, 1.0, linear), // not used
                    Triple(-0.5 pos 0.0, -0.5 pos 0.0, linear),
                    0,
                    avenueElevenNoteJumpGetFrame,
                    1.5 pos 0.0
                )
                addAnimation(
                    animBasicCfg,
                    89285,
                    89523 - 89285,
                    Triple(1.0, 1.0, linear), // not used
                    Triple(-0.5 pos 0.0, -0.5 pos 0.0, linear),
                    0,
                    avenueElevenNoteJumpGetFrame,
                    -0.5 pos 0.0
                )
            }
        }.writeToFolder(File(File("."), "result"))
    }

}