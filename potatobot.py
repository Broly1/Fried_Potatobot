import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# data value
miles_rate = 0.51
stors_rate = 10.00
deadstack_cases_rate = 00.10
casecount_carted_rate = 0.05
pre_postrip_rate = 6.00
intertripe_inspection_rate = 4.50
repositions_drop_hooks_rate = 4.50
hourlly_delay_rate = 13.15
meeting_dalay_rate = 21.00


def menu(update: Update, context: CallbackContext) -> int:
    """Send message on `/menu`."""
    # Get user that sent /menu and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("run", callback_data="run"),
            InlineKeyboardButton("exit", callback_data="exit"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Please press run and answer the questions?", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return 1


def run(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    # edit previews message with this text
    query.edit_message_text("miles driven:")
    return 10


def miles_driven(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["miles_driven"] = update.message.text

    update.message.reply_text("How many stors:")
    return 17


def stors_count(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["stors_count"] = update.message.text
    
    update.message.reply_text("How many carted cases:")
    return 18

def casecount_carted(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["casecount_carted"] = update.message.text
    update.message.reply_text("deadstack cases:")
    return 11


def deadstack_cases(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["deadstack_cases"] = update.message.text

    update.message.reply_text("intertrip inspections:")
    return 12


def intertrip_inspections(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["intertrip_inspections"] = update.message.text

    update.message.reply_text("prepostrip inspections:")
    return 13


def prepostrip_inspections(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["prepostrip_inspections"] = update.message.text

    update.message.reply_text("delay time:")
    return 14


def delay_time(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["delay_time"] = update.message.text

    update.message.reply_text("drop or trailer repositions:")
    return 15


def drop_trailer_repositions(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["drop_trailer_repositions"] = update.message.text

    update.message.reply_text("metting delay:")
    return 16


def metting_delay(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data["metting_delay"] = update.message.text
    
    # rate value calculation
    pay = \
        float(user_data["miles_driven"]) * float(miles_rate) + \
        float(user_data["stors_count"]) * float(stors_rate) + \
        float(user_data["casecount_carted"]) * float(casecount_carted_rate) + \
        float(user_data["prepostrip_inspections"]) * float(pre_postrip_rate) + \
        float(user_data["intertrip_inspections"]) * float(intertripe_inspection_rate) + \
        float(user_data["drop_trailer_repositions"]) * float(repositions_drop_hooks_rate) + \
        float(user_data["delay_time"]) * float(hourlly_delay_rate) + \
        float(user_data["metting_delay"]) * float(meeting_dalay_rate)
    update.message.reply_text("Pay: %s" % pay)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    #query = update.callback_query
    #query.answer()
    update.message.reply_text("conversation canceled")
    return ConversationHandler.END


def exit(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text("you chose to leave the conversation")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', menu)],
        states={
            1: [
                CallbackQueryHandler(run, pattern='^run$'),
                CallbackQueryHandler(exit, pattern='^exit$'),
            ],
            10: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, miles_driven),
            ],
            11: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, deadstack_cases),
            ],
            12: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, intertrip_inspections),
            ],
            13: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, prepostrip_inspections),
            ],
            14: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, delay_time),
            ],
            15: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, drop_trailer_repositions),
            ],
            16: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, metting_delay),
            ],
            17: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, stors_count),
            ],
            18: [
                MessageHandler(Filters.regex(
                    r"^[0-9,\.]+$") & ~Filters.command, casecount_carted),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


'''
PEC 
    Miles driven
    Deadstack cases
    Intertrip inspections
    Prepostrip inspections
    Delay time
    Drop or trailer repositions
    Metting delay
    How many stors
    How many carted cases
>>> Pay =
'''
