from collections import deque
input_data = ["1", "2", "3", "2024", ]
prune_mask = 16777215

fh = open("day_22.txt", "r")
input_data = list(map(str.rstrip, fh))

sequence_total_bananas = {}

def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret & prune_mask


def new_secret(secret) -> int:
    x = secret << 6  # multiply by 64
    secret = mix(secret, x)
    secret = prune(secret)
    x = secret >> 5  # int divide by 32
    secret = mix(secret, x)
    x = secret << 11
    secret = mix(secret, x)
    return prune(secret)


def main(data):
    ans = 0
    for secret in map(int, data):
        sequence = deque([])
        seen_sequences = set()
        current_price = int(str(secret)[-1])
        for _ in range(2000):
            secret = new_secret(secret)
            new_price = int(str(secret)[-1])
            delta = new_price - current_price
            current_price = new_price

            sequence.append(delta)
            if len(sequence) > 4:
                sequence.popleft()
            if len(sequence) == 4:
                key = tuple(sequence)
                if key in seen_sequences:
                    continue
                seen_sequences.add(key)
                if key not in sequence_total_bananas:
                    sequence_total_bananas[key] = 0
                sequence_total_bananas[key] += current_price

        ans = ans + secret
    print(ans)
    print(max(sequence_total_bananas.values()))


main(input_data)
