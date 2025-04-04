from django.core.management.base import BaseCommand, CommandError
from api.models.user import User
from api.models.game_state import GameState

# https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/
class Command(BaseCommand):
    help = "Seed the database"

    def add_arguments(self, parser):
        parser.add_argument("num_users", nargs="+", type=int)
        parser.add_argument("max_turns", nargs="+", type=int)

    def handle(self, *args, **options):

        User.objects.all().delete()
        GameState.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS('User and GameState cleared')
        )

        count = 0
        amount = options["num_users"][0]
        users = []
        while(count < amount):
            last_user_id = count + 1
            new_username = f"User-{last_user_id}"
            user = User.objects.create(user_name = new_username)
            count = count + 1
            users.append(user)
            user.save()
            
        self.stdout.write(
            self.style.SUCCESS('%s Users created' % amount)
        )

        for user in users:
            min_turn = 1
            max_turn = options["max_turns"][0]
            for turn in range(min_turn, max_turn+1):
                map = "[[null,[6,0,0]],[[21,0,0],[12,0,0]],[[4,0,0],null]]"
                game_state = GameState.objects.create(user = user, turn = turn, map=map)
                game_state.save()

        gane_states_made = options["num_users"][0] * options["max_turns"][0]

        self.stdout.write(
            self.style.SUCCESS('%s GameStates created' % gane_states_made)
        )