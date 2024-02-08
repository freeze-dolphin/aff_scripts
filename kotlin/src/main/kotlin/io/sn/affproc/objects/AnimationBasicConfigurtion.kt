package io.sn.affproc.objects

data class AnimationBasicConfigurtion(

    /**
     * animation quality
     */
    val frameCount: Int,

    /**
     * animation speed
     */
    val bpm: Double,

    /**
     * song length
     */
    val noteOffset: Long,
)
