from dotenv import load_dotenv
from agent import CareerAgent

# .envファイルからAPIキーを環境変数に読み込む
load_dotenv()


def main():
    agent = CareerAgent()

    print("Career Agent へようこそ。")
    print("転職に関して何でも聞いてください。")
    print("終了するには 'exit' または 'quit' と入力してください。")
    print("-" * 50)

    while True:
        # ユーザー入力を受け取る
        user_input = input("\nあなた: ").strip()

        # 終了コマンド
        if user_input.lower() in ["exit", "quit"]:
            print("終了します。")
            break

        # 空入力はスキップ
        if not user_input:
            continue

        # Agentに投げて返答をもらう
        reply, usage = agent.chat(user_input)

        print(f"\nAgent: {reply}")
        print(f"\n[tokens] input: {usage.prompt_tokens}, output: {usage.completion_tokens}, total: {usage.total_tokens}")


if __name__ == "__main__":
    main()
