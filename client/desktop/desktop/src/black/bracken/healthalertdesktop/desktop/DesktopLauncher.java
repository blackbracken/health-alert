package black.bracken.healthalertdesktop.desktop;

import black.bracken.healthalertdesktop.HealthAlertDesktop;
import com.badlogic.gdx.backends.lwjgl.LwjglApplication;
import com.badlogic.gdx.backends.lwjgl.LwjglApplicationConfiguration;

public class DesktopLauncher {

    public static void main(String[] arg) {
        LwjglApplicationConfiguration config = new LwjglApplicationConfiguration();
        new LwjglApplication(new HealthAlertDesktop(), config);
    }

}
