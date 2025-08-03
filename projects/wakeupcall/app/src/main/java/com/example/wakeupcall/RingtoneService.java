package com.example.wakeupcall;

import android.app.Service;
import android.content.Intent;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.IBinder;
import android.app.Notification;

public class RingtoneService extends Service {
    private Ringtone ringtone;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // Create a foreground notification
        Notification.Builder builder;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            builder = new Notification.Builder(this, "ALARM_CHANNEL");
        } else {
            builder = new Notification.Builder(this);
        }

        Notification notification = builder.setSmallIcon(@android:drawable/stat_notify_call_mute)
                                          .setContentTitle("Alarm Ringing")
                                          .setContentText("Your alarm is playing.")
                                          .build();

        startForeground(1, notification);

        // Play the default ringtone
        Uri ringtoneUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM);
        ringtone = RingtoneManager.getRingtone(this, ringtoneUri);
        ringtone.play();

        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (ringtone != null && ringtone.isPlaying()) {
            ringtone.stop();
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
