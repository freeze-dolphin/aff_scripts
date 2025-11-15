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
                chart.configuration.tuneOffset(-660)
                timing(
                    offset = 0,
                    bpm = 126,
                    beats = 4,
                )

                val globalOffset = 260279L

                comment {
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
    fun traceCollapse() {
        mapSet {
            difficulties.future {
                chart.configuration.tuneOffset(-660)
                timing(
                    offset = 0,
                    bpm = 126,
                    beats = 4,
                )

                timingGroup {
                    timing(0, 126, 4)
                    genCollapseTraceGroup(1000, 3000, 1 pos 0, 1 pos 0, 50, easeOutSine, 0.004, 0.0008).forEach {
                        addArcNote(it)
                    }
                }
            }
        }.writeToFolder(File(File("."), "result"))
    }

    @Test
    fun noteJump() {
        mapSet {
            difficulties.beyond {
                chart.configuration.tuneOffset(-660)
                timing(
                    offset = 0,
                    bpm = 126,
                    beats = 4,
                )

                val globalOffset = 260279L

                val animBasicCfg = AnimationBasicConfigurtion(240, 126.toDouble(), globalOffset + 1)

                val timingList = listOf<Long>(
                    78095,
                    78571,
                    79047,
                    79523,
                    80000,
                    80476,
                    80952,
                    81428,
                    81904,
                    82380,
                    82857,
                    83333,
                    83809,
                    84285,
                    84761,
                    85238,
                    85714,
                    85952,
                    86190,
                    86428,
                    86666,
                    86904,
                    87142,
                    87380,
                    87619,
                    87857,
                    88095,
                    88333,
                    88571,
                    88809,
                    89047,
                    89285
                )

                val positionList = listOf(
                    -0.25,
                    0.25,
                    0.75,
                    1.25,
                    1.25,
                    0.75,
                    0.25,
                    -0.25,
                    0.75,
                    0.25,
                    1.25,
                    -0.25,
                    0.75,
                    0.25,
                    1.25,
                    -0.25,
                    0.75,
                    0.75,
                    0.25,
                    0.25,
                    1.00,
                    1.00,
                    0.0,
                    0.0,
                    1.25,
                    1.25,
                    -0.25,
                    -0.25,
                    1.5,
                    1.5,
                    -0.5,
                    -0.5
                )

                repeat(timingList.size - 1) {
                    if (timingList[it + 1] == -1L || timingList[it] == -1L) {
                        return@repeat
                    }

                    if (it == 16) {
                        ARCAEA_COORD_SYSTEM_ZOOM_CONSTANT = 700
                    }

                    addAnimation(
                        animBasicCfg,
                        timingList[it],
                        timingList[it + 1] - timingList[it],
                        Triple(1.0, 1.0, linear), // not used
                        Triple(positionList[it] pos 0, positionList[it] pos 0, linear),
                        0,
                        avenueElevenNoteJumpGetFrame,
                        positionList[it + 1] pos 0
                    )
                }
            }
        }.writeToFolder(File(File("."), "result"))
    }

}