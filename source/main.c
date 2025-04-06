/*===========================================
        GRRLIB (GX Version)
        - Template Code -

        Minimum Code To Use GRRLIB
============================================*/

//Reminder: Screen resolution is 852 × 480 on my Wii.
//Reminder: Screen resolution is 852 × 480 on my Wii.
//Reminder: Screen resolution is 852 × 480 on my Wii.
//Reminder: Screen resolution is 852 × 480 on my Wii.
//Reminder: Screen resolution is 852 × 480 on my Wii.

#include <grrlib.h>

#include <stdlib.h>
#include <time.h>
#include <ogc/system.h>
#include <ogc/lwp_watchdog.h>
#include <wiiuse/wpad.h>


void init(GRRLIB_texImg **background, GRRLIB_texImg **cursor, GRRLIB_texImg **art_cursor, GRRLIB_texImg **Rocket1, GRRLIB_texImg **Rocket2, GRRLIB_texImg **Rocket3, GRRLIB_texImg **Rocket4, float *cur_X, float *cur_Y, float *cur_XSpeed, float *cur_YSpeed, float rocketX[4], float rocketY[4], float rocketSpeedX[4]) {
    // Initialise the Graphics & Video subsystem.
    GRRLIB_Init();

    // Initialise the Wiimotes.
    WPAD_Init();

    // Setup Wiimote IR resolution
    WPAD_SetDataFormat(WPAD_CHAN_ALL, WPAD_FMT_BTNS_ACC_IR);
    WPAD_SetVRes(WPAD_CHAN_ALL, rmode->fbWidth, rmode->xfbHeight);

    // Seed the RNG
    u32 seed = ticks_to_millisecs(gettick());
    srand(seed);

    // Load images
    *background = GRRLIB_LoadTextureFromFile("sd:/images/background.jpg");
    *cursor = GRRLIB_LoadTextureFromFile("sd:/images/cursor.png");
    *art_cursor = GRRLIB_LoadTextureFromFile("sd:/images/cursor.png");
    *Rocket1 = GRRLIB_LoadTextureFromFile("sd:/images/Rocket1.png");
    *Rocket2 = GRRLIB_LoadTextureFromFile("sd:/images/Rocket2.png");
    *Rocket3 = GRRLIB_LoadTextureFromFile("sd:/images/Rocket3.png");
    *Rocket4 = GRRLIB_LoadTextureFromFile("sd:/images/Rocket4.png");

    // Cursor initial position and velocity
    *cur_X = 240;
    *cur_Y = 0;
    *cur_XSpeed = 0;
    *cur_YSpeed = 0;

    // Rocket initial positions and speed
    rocketX[0] = 0; rocketX[1] = 0; rocketX[2] = 0; rocketX[3] = 0;
    rocketY[0] = 0; rocketY[1] = 24; rocketY[2] = 48; rocketY[3] = 70;
    rocketSpeedX[0] = 16; rocketSpeedX[1] = 16; rocketSpeedX[2] = 16; rocketSpeedX[3] = 16;
}


void handleInput(float *x, float *y, float *angle, float *cur_X, float *cur_Y, float *cur_XSpeed, float *cur_YSpeed, int *shouldExit) {
    WPAD_ScanPads();  // Scan the Wiimotes.

    *x = WPAD_Data(0)->ir.x;
    *y = WPAD_Data(0)->ir.y;
    *angle = WPAD_Data(0)->ir.angle;

    if (WPAD_ButtonsDown(0) & WPAD_BUTTON_HOME) {
        *shouldExit = 1;
        return;
    }

    // Gravity
    if (WPAD_ButtonsHeld(0) & WPAD_BUTTON_2) {
        *cur_YSpeed += 0.3f;
        if (*cur_YSpeed >= 10) {
            *cur_YSpeed = 10;
        }
    } else {
        *cur_YSpeed -= 0.4f;
        if (*cur_YSpeed <= -13) {
            *cur_YSpeed = -13;
        }
    }

    if (WPAD_ButtonsHeld(0) & WPAD_BUTTON_UP) {
        *cur_XSpeed = 7;
    }

    if (WPAD_ButtonsUp(0) & (WPAD_BUTTON_UP | WPAD_BUTTON_DOWN)) {
        if (*cur_XSpeed != 0) {
            if (*cur_XSpeed > 0) {
                *cur_XSpeed -= 1;
            } else {
                *cur_XSpeed += 1;
            }
        }
    }

    if (WPAD_ButtonsHeld(0) & WPAD_BUTTON_DOWN) {
        *cur_XSpeed = -7;
    }

    // Update position
    *cur_X -= *cur_XSpeed;
    *cur_Y -= *cur_YSpeed;

    // Boundaries
    if (*cur_X <= 0) {
        *cur_XSpeed = 0;
        *cur_X = 0;
    }
    if (*cur_X >= 816) {
        *cur_XSpeed = 0;
        *cur_X = 816;
    }
    if (*cur_Y <= 0) {
        *cur_YSpeed = 0;
        *cur_Y = 0;
    }
    if (*cur_Y >= 428) {
        *cur_YSpeed = 0;
        *cur_Y = 428;
    }
}


int checkCollision(float x1, float y1, int w1, int h1, float x2, float y2, int w2, int h2) {
    // Check if the rectangles overlap
    return (x1 < x2 + w2 && x1 + w1 > x2 && y1 < y2 + h2 && y1 + h1 > y2);
}


void rockets(float cur_X, float cur_Y, float rocketX[4], float rocketY[4], float rocketSpeedX[4]) {
    for (int i = 0; i < 4; i++) {
        // Move rocket
        rocketX[i] -= rocketSpeedX[i];

        // Wrap rocket to the right side if it goes off the left edge
        if (rocketX[i] < -64) {
            rocketX[i] = 856;
            rocketY[i] = rand() % 456;
        }
    }

    // Check for collisions with the artificial cursor
    for (int i = 0; i < 4; i++) {
        if (checkCollision(cur_X, cur_Y, 36, 52, rocketX[i], rocketY[i], 64, 24)) {
            GRRLIB_Exit();
            exit(0);
        }
    }
}


void render(float x, float y, float angle, float cur_X, float cur_Y, float rocketX[4], float rocketY[4], GRRLIB_texImg *background, GRRLIB_texImg *cursor, GRRLIB_texImg *art_cursor, GRRLIB_texImg *Rocket1, GRRLIB_texImg *Rocket2, GRRLIB_texImg *Rocket3, GRRLIB_texImg *Rocket4) {
    GRRLIB_DrawImg(0, 0, background, 0, 1, 1, RGBA(255, 255, 255, 255));
    GRRLIB_DrawImg(x, y, cursor, angle * (180.0f / M_PI), 1, 1, RGBA(255, 255, 255, 255));
    GRRLIB_DrawImg(cur_X, cur_Y, art_cursor, 0, 1, 1, RGBA(255, 255, 255, 255));

    GRRLIB_DrawImg(rocketX[0], rocketY[0], Rocket1, 0, 1, 1, RGBA(255, 255, 255, 255));
    GRRLIB_DrawImg(rocketX[1], rocketY[1], Rocket2, 0, 1, 1, RGBA(255, 255, 255, 255));
    GRRLIB_DrawImg(rocketX[2], rocketY[2], Rocket3, 0, 1, 1, RGBA(255, 255, 255, 255));
    GRRLIB_DrawImg(rocketX[3], rocketY[3], Rocket4, 0, 1, 1, RGBA(255, 255, 255, 255));
}



int main(int argc, char **argv) {
    // Declare variables
    GRRLIB_texImg *background, *cursor, *art_cursor, *Rocket1, *Rocket2, *Rocket3, *Rocket4;

    float x, y, angle, cur_X, cur_Y, cur_XSpeed, cur_YSpeed, rocketX[4], rocketY[4], rocketSpeedX[4];

    int shouldExit = 0;

    // Initialize everything
    init(&background, &cursor, &art_cursor, &Rocket1, &Rocket2, &Rocket3, &Rocket4, &cur_X, &cur_Y, &cur_XSpeed, &cur_YSpeed, rocketX, rocketY, rocketSpeedX);
    while(1) 
    {
        handleInput(&x, &y, &angle, &cur_X, &cur_Y, &cur_XSpeed, &cur_YSpeed, &shouldExit);
        rockets(cur_X, cur_Y, rocketX, rocketY, rocketSpeedX);
        render(x, y, angle, cur_X, cur_Y, rocketX, rocketY, background, cursor, art_cursor, Rocket1, Rocket2, Rocket3, Rocket4);
        GRRLIB_Render(); // Render the frame buffer to the TV.
    }

    GRRLIB_Exit(); // Clear allocated memory.

    exit(0);  // Use exit() to exit a program, do not use 'return' from main().
}
