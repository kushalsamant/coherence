package com.example.wakeupcall;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.app.Notification;
import android.app.NotificationManager;

public class AlarmReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        // Start the foreground service to play the ringtone
        Intent serviceIntent = new Intent(context, RingtoneService.class);
        context.startForegroundService(serviceIntent);

        // Show full-screen notification
        Intent fullScreenIntent = new Intent(context, CallActivity.class);
        PendingIntent fullScreenPendingIntent = PendingIntent.getActivity(context, 0, fullScreenIntent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

        Notification.Builder builder;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            builder = new Notification.Builder(context, "ALARM_CHANNEL");
        } else {
            builder = new Notification.Builder(context);
        }

        builder.setSmallIcon(@android:drawable/stat_notify_call_mute)
               .setContentTitle("Alarm")
               .setContentText("Your alarm is ringing!")
               .setPriority(Notification.PRIORITY_MAX)
               .setCategory(Notification.CATEGORY_CALL)
               .setFullScreenIntent(fullScreenPendingIntent, true);

        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(1, builder.build());
    }
}
