#!/usr/bin/env python3
# coding: utf-8

# ----------------------------------------------------------------------------
# Created By  : Yusuke Kawatsu
# Created Date: 2023/05/31
# Usage       : python3 debug_cmd.py <linux command separated by spaces>
#               python3 debug_cmd.py -c '<linux command on shell>'
# Description : Debug linux command error by using GPT/LLM.
# ---------------------------------------------------------------------------

import os
import sys
import locale
import argparse
import platform
import subprocess
from typing import Union
from typing import Generator

import openai


# CLI encoding.
_CLI_ENCODING = locale.getpreferredencoding()


def main() -> None:
    """
    Entry point.
    """
    _assert_environment_variables()
    commands = _load_cli_args()

    return_code, cmd_out = _exec_command(commands)

    if return_code == 0:
        print('\n-------- コマンドは成功しました --------')
        sys.exit(0)

    print('\n-------- エラー原因を解析中 --------')
    cmd_str = ' '.join(commands) if type(commands) is list else commands
    answer = _ask_llm_about_error(cmd=cmd_str, error_message=cmd_out)
    print(answer)


def _assert_environment_variables() -> None:
    """
    ensure essential environment variables.
    """
    environments = ['OPENAI_API_KEY']

    for e in environments:
        if e not in os.environ:
            sys.stderr.write(f'Please set environment variable "{e}".')
            sys.exit(1)


def _load_cli_args() -> Union[str, list[str]]:
    """
    Parse CLI arguments.

    :return: command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog='debug_cmd',
        description='Debug linux command error by using GPT/LLM.',
    )

    parser.add_argument('command', nargs='*', type=str, help='command and arguments separated by spaces. cannot use pipe(|), redirect(>), etc.')  # nopep8
    parser.add_argument('-c', type=str, help='shell string like "sh -c ..."')
    args = parser.parse_args()

    if not args.command and not args.c:
        parser.print_help()
        sys.exit(1)

    return args.c if args.c else [arg for arg in args.command if arg]


def _exec_command(cmd: Union[str, list[str]]) -> (int, str):
    """
    :param cmd: command line arguments.
    :return: (return code, stdout+stderr)
    """
    env = os.environ.copy()
    cwd = os.getcwd()

    # commands が list か str (-c option) かで、shell を経由するかどうか分けてる.
    proc = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) \
        if type(cmd) is list \
        else subprocess.Popen(cmd, shell=True, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def _print(text: str) -> str:
        sys.stdout.write(text)
        return text

    # print & concat.
    lines = ''.join([_print(line) for line in _get_stdout_by_lines(proc)])

    return proc.returncode, lines


def _get_stdout_by_lines(proc: subprocess.Popen) -> Generator[str, None, None]:
    """
    :param proc: sub process.
    :return: 標準出力 (行毎).
    """
    while True:
        line = proc.stdout.readline()

        if not line and proc.poll() is not None:
            break

        yield line.decode(_CLI_ENCODING)


def _ask_llm_about_error(cmd: str, error_message: str) -> str:
    """
    Entry point.

    :param cmd: command line arguments.
    :param error_message: command error message.
    :return: answer.
    """
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': 'あなたは Mac, Unix, Linux のターミナル上で発生したコマンドのエラーの解消を手助けする AI アシスタントです'},
            {'role': 'assistant', 'content': 'あなたの使っているパソコンの OS名, OSバージョン を教えて下さい'},
            {'role': 'user', 'content': f'私のパソコンは {_get_os()} です'},
            {'role': 'assistant', 'content': 'エラーが発生したコマンドを教えて下さい'},
            {'role': 'user', 'content': cmd},
            {'role': 'assistant', 'content': 'エラーが発生したコマンドのエラーメッセージを教えて下さい'},
            {'role': 'user', 'content': error_message},
            {'role': 'assistant', 'content': 'コマンドのエラーの原因が分かりました。以下にエラーの原因とその解決策を示します。追加の質問は受付しません'},
        ]
    )

    # print the chat completion
    return chat_completion.choices[0].message.content


def _get_os() -> str:
    """
    :return: '{OS name} {OS version}'.
    """
    os_name = platform.system()
    os_version = platform.version()

    if os_name != 'Darwin':
        return f'{os_name} {os_version}'

    mac_ver, _, arch = platform.mac_ver()
    return f'macOS {mac_ver} ({arch})'


if __name__ == '__main__':
    main()
