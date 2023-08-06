WATERING_REQUEST_NAME = 'watering'
POSITION_POST_NAME = 'spider_position'
MESSAGE_POST_NAME = 'message'

REQUEST_WATERING_INSTRUCTION_ADDR = f"http://192.168.1.20:5000/{WATERING_REQUEST_NAME}"
POST_SPIDER_POSITION_ADDR = f"http://192.168.1.20:5000/{POSITION_POST_NAME}"
POST_STATE_MESSAGE_ADDR = f"http://192.168.1.20:5000/{MESSAGE_POST_NAME}"

MICROSWITCH_ERROR = "E01"
VOLTAGE_DROP_ERROR = "E02"
STARTUP_SINGULARITY_ERROR = "E03"
BREAKS_ACTIVATED_ERROR = "E04"
ALL_LEGS_NOT_ATTACHED_ERROR = "E05"
AUTO_CORRECITON_ERROR = "E06"
GRIPPER_ERROR = "E07"

ERROR_IN_MOTOR_WARNING = "W01"
LEG_CLOSE_TO_SINGULARITY_WARNING = "W02"
LEG_MISSED_PIN_WARNING = "W03"
TEMPERATURES_IN_MOTORS_TOO_HIGH_WARNING = "W04"

WORKING_PHASE_STARTED_MESSAGE = "M01"
WORKING_PHASE_FINISHED_MESSAGE = "M02"
TRANSITIONING_TO_RESTING_PHASE_MESSAGE = "M03"
RESTING_PHASE_STARTED_MESSAGE = "M04"
RESTING_PHASE_FINISHED_MESSAGE = "M05"
AUTO_CORRECTION_SUCCESSFUL_MESSAGE = "M06"
REFILLING_STARTED_MESSAGE = "M07"
REFILLING_FINISHED_MESSAGE = "M08"
WATERING_STARTED_MESSAGE = "M09"
WATERING_FINISHED_MESSAGE = "M10"
LEG_IN_MANUAL_CORRECTION_MODE_MESSAGE = "M11"
REBOOTING_MOTORS_MESSAGE = "M12"
LEG_MOVE_MESSAGE = "M13"

MANUALLY_MOVE_LEG_ON_PIN_INSTRUCTION = "I01"

# TODO: Add messages for enable-disable action.
STATUS_CODES_DICT = {
    MICROSWITCH_ERROR: "Microswitch stucked.",
    # TODO: Not used yet.
    VOLTAGE_DROP_ERROR: "Voltage droped below *.",
    STARTUP_SINGULARITY_ERROR: "Possible singularity on startup.",
    # TODO: Not used yet.
    BREAKS_ACTIVATED_ERROR: "Breaks are still activated.",
    ALL_LEGS_NOT_ATTACHED_ERROR: "One or more legs are not attached. Cannot move selected leg.",
    AUTO_CORRECITON_ERROR: "Auto-correction was not succesful. Entering manual-correction mode.",
    GRIPPER_ERROR: "Gripper did not open correctly.",

    ERROR_IN_MOTOR_WARNING: "Hardware error in motor.",
    # TODO: Not used yet.
    LEG_CLOSE_TO_SINGULARITY_WARNING: "Leg is close to singularity.",
    LEG_MISSED_PIN_WARNING: "Leg missed the pin. Entering auto-correction mode.",
    TEMPERATURES_IN_MOTORS_TOO_HIGH_WARNING: "Temperature in one or more motors is above allowed value.",

    WORKING_PHASE_STARTED_MESSAGE: "Working phase has started.",
    WORKING_PHASE_FINISHED_MESSAGE: "Working phase has finished.",
    TRANSITIONING_TO_RESTING_PHASE_MESSAGE: "Transitioning into resting phase.",
    RESTING_PHASE_STARTED_MESSAGE: "Resting phase has started.",
    RESTING_PHASE_FINISHED_MESSAGE: "Resting phase has finished.",
    AUTO_CORRECTION_SUCCESSFUL_MESSAGE: "Auto-correction was successful.",
    REFILLING_STARTED_MESSAGE: "Refilling the water tank has started.",
    REFILLING_FINISHED_MESSAGE: "Refilling the water tank has finished.",
    WATERING_STARTED_MESSAGE: "Watering has started.",
    WATERING_FINISHED_MESSAGE: "Watering has finished.",
    LEG_IN_MANUAL_CORRECTION_MODE_MESSAGE: "Leg is in manual-correction mode.",
    REBOOTING_MOTORS_MESSAGE: "Rebooting motors in error.",
    LEG_MOVE_MESSAGE: "Leg has moved."
}

def create_instruction_message(*instruction_args) -> str:
    """Create instruction message, based on given parameters. First parameter should always be the instruction code. Following parameters
    are specific for each instruction:
    - MANUALLY_MOVE_LEG_ON_PIN_INSTRUCTION: 2nd parameter is leg id, 3rd is pin id.
    - WATERING_INSTRUCTION: 2nd parameter is (x, y) position, 3rd is action, 4th is millilitres.
        - action is 0 for watering and 1 for refilling.

    Returns:
        string: Instruction message.
    """
    return ",".join(map(str, list(instruction_args)))
