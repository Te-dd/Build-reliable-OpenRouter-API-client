from ai_client import ask_ai, APIError

def main():

    print("=" * 40)
    print("DAY 4 ;RELIABLE AI API CLIENT")
    print("=" * 40 )
    total_tokens_used = 0
    while True:

        question = input ("\nAsk a question, or type exit:")

        if question.lower().strip() == "exit":
            print("Exiting the program.")
            break

        try:
            result = ask_ai(question)
            print("\nAI RESPONSE:")
            print(result["answer"])

            print("\nREQUEST DETAILS:")
            print("Model:", result["model"])
            print("Response time:", result["response_time"], "seconds")
            print("Usage:", result["usage"])
            print("Generation ID:", result["generation_id"])

            usage = result["usage"]

            tokens = usage.get("total_tokens", 0)

            total_tokens_used += tokens

            print("Tokens used in this request:", tokens)
            print("Total tokens used today in this session:", total_tokens_used)

        except ValueError as error:
            print("Input error:", error)

        except APIError as error:
            print("API error:", error)


if __name__ == "__main__":
    main()