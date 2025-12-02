package com.example.wakeup;

import android.app.Activity;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Vibrator;
import android.view.WindowManager;
import android.widget.TextView;

public class AlarmReceiver extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED |
                             WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON |
                             WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        TextView textView = new TextView(this);
        textView.setText("Wake up!");
        textView.setTextSize(40);
        setContentView(textView);

        Vibrator v = (Vibrator) getSystemService(VIBRATOR_SERVICE);
        if (v != null) v.vibrate(1000);

        MediaPlayer mediaPlayer = MediaPlayer.create(this, android.provider.Settings.System.DEFAULT_ALARM_ALERT_URI);
        mediaPlayer.start();
    }
}