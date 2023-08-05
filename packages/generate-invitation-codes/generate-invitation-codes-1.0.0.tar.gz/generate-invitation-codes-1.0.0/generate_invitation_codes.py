#!/usr/bin/env python
import argparse
import secrets


class GlobalTrialManager:
    def __init__(self):
        self.code_storage = {}

    def create_codes(self, email, n, code_length):
        codes = [secrets.token_hex(code_length // 2) for _ in range(n)]
        self.code_storage[email] = codes
        return codes


global_trial_manager = GlobalTrialManager()


def generate_invitation_codes(email, n, code_length=16):
    return global_trial_manager.create_codes(email, n, code_length)


def parse_args():
    parser = argparse.ArgumentParser(description='Generate invitation codes for global trial usage.')
    parser.add_argument('email', help='The email to bind the generated codes to.')
    parser.add_argument('--num', '-n', type=int, default=5, help='The number of invitation codes to generate.')
    parser.add_argument('--length', '-l', type=int, default=16,
                        help='The length of the generated invitation codes (default=16).')

    return parser.parse_args()


def main():
    args = parse_args()

    codes = generate_invitation_codes(args.email, args.num, args.length)
    print(f'Generated invitation codes for {args.email}:')
    for code in codes:
        print(f'  {code}')


if __name__ == '__main__':
    main()
