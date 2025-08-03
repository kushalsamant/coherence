package com.example.wakeupcall;

import android.app.Activity;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TimePicker;
import android.widget.Toast;
import java.util.Calendar;

public class MainActivity extends Activity {
    private TimePicker timePicker;
    private Button setAlarmButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Create notification channel
        createNotificationChannel();

        timePicker = findViewById(R.id.timePicker);
        setAlarmButton = findViewById(R.id.setAlarmButton);

        setAlarmButton.setOnClickListener(v -> {
            Calendar calendar = Calendar.getInstance();
            calendar.set(Calendar.HOUR_OF_DAY, timePicker.getCurrentHour());
            calendar.set(Calendar.MINUTE, timePicker.getCurrentMinute());
            calendar.set(Calendar.SECOND, 0);

            if (calendar.getTimeInMillis() <= System.currentTimeMillis()) {
                calendar.add(Calendar.DAY_OF_MONTH, 1);
            }

            setAlarm(calendar.getTimeInMillis());
            Toast.makeText(this, "Alarm set for " + calendar.getTime(), Toast.LENGTH_LONG).show();
        });
    }

    private void createNotificationChannel() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    "ALARM_CHANNEL",
                    "Alarm Notifications",
                    NotificationManager.IMPORTANCE_HIGH);
            channel.setDescription("Channel for alarm notifications");
            NotificationManager notificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(channel);
        }
    }

    private void setAlarm(long triggerAtMillis) {
        AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
        Intent intent = new Intent(this, AlarmReceiver.class);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(this, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

        if (alarmManager != null) {
            alarmManager.setExact(AlarmManager.RTC_WAKEUP, triggerAtMillis, pendingIntent);
        }
    }
}
