package com.example.wakeupcall;

import android.app.Activity;
import android.os.Bundle;
import android.view.WindowManager;
import android.widget.Button;

public class CallActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_call);

        // Show activity even on lock screen
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED |
                WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD |
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON |
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON);

        Button acceptButton = findViewById(R.id.acceptButton);
        Button declineButton = findViewById(R.id.declineButton);

        acceptButton.setOnClickListener(v -> {
            stopRingtoneService();
            finish();
        });

        declineButton.setOnClickListener(v -> {
            stopRingtoneService();
            finish();
        });
    }

    private void stopRingtoneService() {
        Intent intent = new Intent(this, RingtoneService.class);
        stopService(intent);
    }
}
