package black.bracken.healthalertandroid

import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Handler
import android.os.IBinder

class AlertService : Service() {

    companion object {
        private const val NOTIFICATION_ID = 1987
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        return START_STICKY
    }

    private fun update() {
        

        Handler().postDelayed({
            update()
        }, 10 * 1000L)
    }

}