from board import Board
from openai import OpenAI
import os
import json
import re


class AiPlayer:

    def __init__(self, game, board):
        self.settings = game.settings
        self.board = board
        self.ai_client = OpenAI(api_key=os.environ.get(self.settings.ai_key_env_variable))

    def make_move(self):
        attempt = 1
        while attempt < 11:
            try:
                response = self._request_ai_()
                pattern = re.compile('{.*}')
                match = pattern.search(response.lower())
                move = json.loads(match.group())
                print(f"Received AI move: {move}")

                return move["x"], move["y"]

            except Exception as e:
                print(f"Will retry to get AI move. Attempt {attempt}. Exception {e}")
                attempt += 1

        raise Exception(f"Can't got AI move in {attempt} attempts")

    def _request_ai_(self):
        whites = self.board.white_dot_matrix_positions()
        blacks = self.board.black_dot_matrix_positions()
        empties = self.board.empty_dot_matrix_positions()

        completion = self.ai_client.chat.completions.create(
            model=self.settings.ai_model,
            messages=[
                {"role": "system", "content": """
                        You play Gomoku. The board size is 15*15. You play white. 
                        You receive list of blacks, whites and empties positions on the board as (x,y) pairs. 
                        You should make the best move to win. 
                        Provide your response in json format like {"x"=7,"y"=5}

                        Input example:
                            whites=[(6,7)]
                            blacks=[(5,5), (6,5)]
                            empties = [(4,4),(6,6), ... , (15,15)]

                        Response example: {"x"=6, "y"=6}
                        """},
                {"role": "user", "content": f"""
                        The current position on the board:
                        whites={whites},
                        blacks={blacks},
                        empties={empties}

                        You play white. Make the best move to win.
                        Be concise and respond only with coordinates without any comments. 
                        """}
            ]
        )

        return completion.choices[0].message.content.lower()
