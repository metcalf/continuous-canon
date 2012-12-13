// Delays and timing
#define FEED_DELAY 50 // Delay between the feed sensor trip and registering the paper feed
#define OFF_DELAY 20 // Milliseconds between pulses for the motor to be considered off
#define MAX_FEED_TIME 1500 // Never allow a feed longer than this
#define MIN_FEED_TIME 50 // Minimum time paper must move to be considered fed
#define CLEAR_FEED_TIME 500 // Time motor must remain on to count as a feed out
#define START_WAIT_TIME 1000 // Time motor must remain off to assume printer is ready to start printing
#define CLEAR_WAIT_TIME 3000 // Time motor must remain off to assume printer is ready to clear
#define PWR_TIME 2000 // Time for power light to be in a state to be considered ON/OFF
#define SLEEP_DELAY 1000*60*3 // Shut off the printer after 3 minutes in print disabled
#define PWR_BUTTON_DELAY 100 // Time to hold down power button
#define MIN_MOTOR_TIME 15 // Minimum running time considered valid start/stop

#define START_PULSES 15 // Number of pulses received before registering a motor start, signal can be noisy

// Servo positions
#define ON_FRONT_SERVO 35
#define OFF_FRONT_SERVO 15
#define ON_BACK_SERVO 65
#define OFF_BACK_SERVO 115

#define FEED_PIN 2
#define PAPER_PIN 5
#define FRONT_SERVO_PIN 4
#define BACK_SERVO_PIN 6
#define PWR_BUTTON_PIN 7
#define ERR_LIGHT_PIN 10
#define PWR_LIGHT_PIN 9

#define FEED_INT 0
#define MOTOR_INT 1

enum STATES {
  OFF=0,
  STARTSTOP=1,
  STANDBY=2,
  READY=3,
  FED=4,
  PRINT=5,
  CLEAR=6,
  ERROR=7,
};

enum INPUTS {
  PWR_LIGHT = 0,
  ERR_LIGHT = 1,
  MOTOR = 2,
  FEED = 3,
  SERIAL_READ = 4,
};

enum COMMANDS {
  // Input commands
  PRINT_DISABLE = 0,
  PRINT_ENABLE = 1,
  PRINT_START = 2,
  PRINT_FINISH = 3
  
  // Output commands
};

struct InputState{
  char state;
  unsigned long start;
};
