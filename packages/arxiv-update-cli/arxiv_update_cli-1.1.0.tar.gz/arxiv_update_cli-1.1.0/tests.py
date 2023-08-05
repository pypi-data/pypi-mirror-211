#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Juliette Monsel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Tests
"""

import unittest
from unittest import mock
import arxiv_update_cli as pkg
from datetime import datetime, timedelta
import io
import contextlib
import tempfile
import os
import smtplib
import types
import time
import threading

test_config = {
    "General": {
        "categories": "quant-ph",
        "keywords": "quantum, machine learning",
        "authors": "Jane Doe, Paul Smith",
        "sort_by": "submittedDate",
        "last_update": f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}",
        "format": "full",
    },
    "Email": {
        "smtp_server": "",
        "smtp_port": "465",
        "email": "",
    }
}


def mock_feed_entry(date):
    return {"updated_parsed": date.timetuple(), "published_parsed": (date - timedelta(days=7)).timetuple()}


class TestArxivUpdateCLI(unittest.TestCase):
    def setUp(self):
        pkg.CONFIG.update(**test_config)

    def test_input(self):
        try:
            import msvcrt
        except ImportError:

            def inputfunc(prompt):
                time.sleep(2)
                return "input"

            with mock.patch('arxiv_update_cli.input', create=True) as mock_input:
                mock_input.side_effect = inputfunc
                with self.assertRaises(TimeoutError):
                    pkg.input_timeout(">>>", 1)

                mock_input.return_value = "input"
                self.assertEqual("input", pkg.input_timeout(">>>", 3))

        else:  # windows
            from pynput.keyboard import Key, Controller

            with self.assertRaises(TimeoutError):
                pkg.input_timeout(">>>", 1)
            time.sleep(2)

            def mock_input():
                time.sleep(1)
                keyboard = Controller()
                keyboard.press("a")
                keyboard.release("a")
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)

            threading.Thread(target=mock_input).start()
            self.assertEqual("a", pkg.input_timeout(">>>", 3))

    def test_config(self):
        file1 = tempfile.mktemp(suffix='.ini', prefix='config', dir=None)
        file2 = tempfile.mktemp(suffix='.ini', prefix='config', dir=None)
        pkg.CONFIG_PATHS.clear()
        pkg.CONFIG_PATHS.extend([file1, file2])

        # config loading
        with self.assertRaises(SystemExit) as exc: # no config file exists
            pkg.load_default_config()
        self.assertFalse(exc.exception.code)
        # file2 has been created
        self.assertEqual(pkg.load_default_config(), file2)
        pkg.CONFIG.set("General", "keywords", "test1")
        # save config to file1
        pkg.save_config(file1)
        pkg.CONFIG.set("General", "keywords", "test2")
        # save modified config to file2
        pkg.save_config(file2)
        # reload config
        self.assertEqual(pkg.load_default_config(), file2)
        self.assertEqual(pkg.CONFIG.get("General", "keywords"), "test2")

        os.remove(file2)
        # reload config
        self.assertEqual(pkg.load_default_config(), file1)
        self.assertEqual(pkg.CONFIG.get("General", "keywords"), "test1")

        os.remove(file1)

    def test_parsing(self):
        # default
        args = pkg.parser.parse_args([])
        self.assertFalse(args.email)
        self.assertFalse(args.log)
        self.assertFalse(args.version)
        self.assertIsNone(args.since)
        self.assertIsNone(args.config)
        self.assertIsNone(args.subcmd)
        self.assertIsNone(args.output)
        # help message
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-h"])
        self.assertEqual(exc.exception.code, 0)
        # email
        args = pkg.parser.parse_args(["-e"])
        self.assertTrue(args.email)
        # log
        args = pkg.parser.parse_args(["--log"])
        self.assertTrue(args.log)
        # version
        args = pkg.parser.parse_args(["-v"])
        self.assertTrue(args.version)
        # since
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-s"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["-s", "2022-10-01"])
        self.assertEqual(args.since, datetime(2022, 10, 1))
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-s", "01/10/2022"])
        self.assertEqual(exc.exception.code, 2)
        # config
        args = pkg.parser.parse_args(["-c"])
        self.assertEqual(args.config, "")
        args = pkg.parser.parse_args(["-c", "/path"])
        self.assertEqual(args.config, "/path")
        # output
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-o"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["-o", "/path"])
        self.assertEqual(args.output, "/path")
        # display
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-f"])
        self.assertEqual(exc.exception.code, 2)
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["-f", "test"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["-f", "id"])
        self.assertEqual(args.display, "id")
        # query
        ## no args
        args = pkg.parser.parse_args(["query"])
        self.assertEqual(args.subcmd, "query")
        self.assertEqual(args.search_query, "")
        self.assertFalse(args.query_help,)
        self.assertFalse(args.id_list)
        self.assertEqual(args.sort_by, 'lastUpdatedDate')
        self.assertEqual(args.sort_order, 'descending')
        self.assertIsNone(args.start_date)
        self.assertIsNone(args.end_date)
        self.assertIsNone(args.max_results)
        ## search query
        args = pkg.parser.parse_args(["query", "search_query"])
        self.assertEqual(args.search_query, "search_query")
        ## query help
        args = pkg.parser.parse_args(["query", "--api-query-help"])
        self.assertTrue(args.query_help)
        ## help message
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "-h"])
        self.assertEqual(exc.exception.code, 0)
        ## id list
        args = pkg.parser.parse_args(["query", "--id-list", "a", "b", "c"])
        self.assertEqual(args.id_list, list("abc"))
        ## sort by
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--sort-by"])
        self.assertEqual(exc.exception.code, 2)
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--sort-by", "test"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["query", "--sort-by", "relevance"])
        self.assertEqual(args.sort_by, "relevance")
        ## sort order
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--sort-order"])
        self.assertEqual(exc.exception.code, 2)
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--sort-order", "test"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["query", "--sort-order", "ascending"])
        self.assertEqual(args.sort_order, "ascending")
        ## start date
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--start-date"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["query", "--start-date", "2022-10-01"])
        self.assertEqual(args.start_date, datetime(2022, 10, 1))
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--start-date", "01/10/2022"])
        self.assertEqual(exc.exception.code, 2)
        ## end date
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--end-date"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["query", "--end-date", "2022-10-01"])
        self.assertEqual(args.end_date, datetime(2022, 10, 1))
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--end-date", "01/10/2022"])
        self.assertEqual(exc.exception.code, 2)
        ## max results
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--max-results"])
        self.assertEqual(exc.exception.code, 2)
        args = pkg.parser.parse_args(["query", "--max-results", "2"])
        self.assertEqual(args.max_results, 2)
        with self.assertRaises(SystemExit) as exc:
            args = pkg.parser.parse_args(["query", "--max-results", "a"])
        self.assertEqual(exc.exception.code, 2)

    @mock.patch('arxiv_update_cli.api_query', mock.Mock(return_value=[]), create=True)
    @mock.patch('arxiv_update_cli.api_general_query', mock.Mock(return_value=[]), create=True)
    @mock.patch('arxiv_update_cli.format_entry', mock.Mock(side_effect=lambda article, display: article), create=True)
    @mock.patch('arxiv_update_cli.send_email', mock.Mock(), create=True)
    def test_main(self):
        outfile = tempfile.mktemp(suffix='.txt', dir=None)

        # version
        stdout = io.StringIO()
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stdout(stdout):
            pkg._main(["-v"])
        self.assertTrue(pkg.VERSION in stdout.getvalue())
        self.assertFalse(exc.exception.code)
        # log
        stdout = io.StringIO()
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stdout(stdout):
            pkg._main(["--log"])
        self.assertTrue(pkg.PATH_LOG in stdout.getvalue())
        self.assertFalse(exc.exception.code)
        # log
        stdout = io.StringIO()
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stdout(stdout):
            pkg._main(["--log"])
        self.assertTrue(pkg.PATH_LOG in stdout.getvalue())
        self.assertFalse(exc.exception.code)
        # config
        file1 = tempfile.mktemp(suffix='.ini', prefix='config', dir=None)
        file2 = tempfile.mktemp(suffix='.ini', prefix='config', dir=None)
        pkg.CONFIG_PATHS.clear()
        pkg.CONFIG_PATHS.extend([file1])
        with self.assertRaises(SystemExit) as exc: # no config file exists
            pkg._main(["-c"])
        self.assertFalse(exc.exception.code)
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stdout(stdout):
            pkg._main(["-c"])
        self.assertTrue(file1 in stdout.getvalue())
        self.assertFalse(exc.exception.code)
        last_update = pkg.CONFIG.get("General", "last_update")
        with self.assertLogs() as captured:
            pkg._main(["-c", file2])
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.assertEqual(len(captured.records), 2)
            self.assertTrue("Invalid config file" in captured.records[0].getMessage())
            self.assertEqual(captured.records[0].args[0], file2)
            self.assertEqual(f"No new articles since {last_update}.", captured.records[1].getMessage())
        self.assertEqual(now, pkg.CONFIG.get("General", "last_update"))
        pkg.CONFIG.set("General", "last_update", "a")
        pkg.save_config(file1)
        # execution without arguments (wrong last_update date)
        with self.assertLogs() as captured:
            pkg._main([])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(f"No new articles since {(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M')}.", captured.records[-1].getMessage())
        pkg._main(["-e"])
        pkg.send_email.assert_not_called()  # no update to send
        self.assertFalse(os.path.exists(outfile))
        pkg._main(["-o", outfile])
        self.assertFalse(os.path.exists(outfile)) # no update to write
        # since
        with self.assertLogs() as captured:
            pkg._main(["-s", "2022-01-01"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual("No new articles since 2022-01-01 00:00.", captured.records[-1].getMessage())

        # with articles
        ## stdout
        pkg.api_query.return_value = ["a", "b", "c"]
        stdout = io.StringIO()
        with self.assertLogs() as captured, contextlib.redirect_stdout(stdout):
            pkg._main(["-f", "condensed"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(f"\033[3m%% 3 new articles since {pkg.CONFIG.get('General', 'last_update')}\033[0m.", captured.records[-1].getMessage())
        pkg.send_email.assert_not_called()
        pkg.format_entry.assert_called_with("c", "condensed")
        self.assertEqual("a\nb\nc\n", stdout.getvalue())
        ## email
        last_update = pkg.CONFIG.get('General', 'last_update')
        header = f"arXiv update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        footer = f"\033[3m%% 3 new articles since {last_update}\033[0m."
        stdout = io.StringIO()
        with self.assertLogs() as captured, contextlib.redirect_stdout(stdout):
            pkg._main(["-e"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(f"\033[3m%% 3 new articles since {last_update}\033[0m.", captured.records[-1].getMessage())
        pkg.send_email.assert_called_once_with("a\nb\nc\n" + footer, header)
        pkg.format_entry.assert_called_with("c", None)
        self.assertEqual("a\nb\nc\n", stdout.getvalue())
        ## output
        last_update = pkg.CONFIG.get('General', 'last_update')
        header = f"arXiv update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        footer = f"\033[3m%% 3 new articles since {last_update}\033[0m."
        stdout = io.StringIO()
        with self.assertLogs() as captured, contextlib.redirect_stdout(stdout):
            pkg._main(["-o", outfile])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(f"\033[3m%% 3 new articles since {last_update}\033[0m.", captured.records[-1].getMessage())
        pkg.send_email.assert_called_once()  # called from previous exec
        self.assertEqual("", stdout.getvalue())
        self.assertTrue(os.path.exists(outfile))
        with open(outfile) as file:
            txt = file.read()
        print(txt)
        self.assertFalse("\033[0m" in txt)
        self.assertTrue(txt.startswith(header))
        self.assertTrue(txt.endswith(pkg.ansi_regexp.sub("", footer)))
        self.assertTrue("a\nb\nc\n" in txt)
        os.remove(outfile)

        # general query
        pkg.send_email.reset_mock()
        ## query help
        stdout = io.StringIO()
        with self.assertRaises(SystemExit) as exc, contextlib.redirect_stdout(stdout):
            pkg._main(["query", "--api-query-help"])
        self.assertTrue(pkg.API_DOC in stdout.getvalue())
        self.assertFalse(exc.exception.code)
        ## no args
        with self.assertLogs() as captured:
            pkg._main(["query"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual("No article found.", captured.records[-1].getMessage())
        pkg.api_general_query.assert_called_once_with(search_query="", id_list=[],
                                                      sort_by='lastUpdatedDate', sort_order='descending',
                                                      start_date=None, end_date=None, max_results=None)
        # args
        with self.assertLogs() as captured:
            pkg._main(["query", "test", "--id-list", "1", "2", "--max-results",
                       "10", "--sort-order", "ascending", "--sort-by", "relevance",
                       "--start-date", "2022-01-01", "--end-date", "2022-06-01"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual("No article found.", captured.records[-1].getMessage())
        pkg.api_general_query.assert_called_with(search_query="test", id_list=["1", "2"],
                                                 sort_by='relevance', sort_order='ascending',
                                                 start_date=datetime(2022, 1, 1), end_date=datetime(2022, 6, 1),
                                                 max_results=10)
        ## with articles
        pkg.api_general_query.return_value = ["a", "b", "c"]
        stdout = io.StringIO()
        with self.assertLogs() as captured, contextlib.redirect_stdout(stdout):
            pkg._main(["-f", "condensed", "query"])
            self.assertEqual(len(captured.records), 1)
            self.assertEqual("\033[3m%% 3 articles found.\033[0m", captured.records[-1].getMessage())
        self.assertEqual("a\nb\nc\n", stdout.getvalue())
        pkg.format_entry.assert_called_with("c", "condensed")

        os.remove(file1)


        # TODO: new arguments for query

    @mock.patch("getpass.getpass", mock.Mock(return_value="mypassword"))
    @mock.patch('arxiv_update_cli.input_timeout', mock.Mock(side_effect=["localhost", "test@mail.com"]), create=True)
    @mock.patch('arxiv_update_cli.get_pwd_from_keyring', mock.Mock(side_effect=[None, "mypassword", "mypassword"]), create=True)
    @mock.patch('arxiv_update_cli.store_pwd_in_keyring', mock.Mock(return_value=None), create=True)
    def test_send(self):

        # email sending -- successfull
        with self.assertLogs() as captured:
            with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
                server = mock_smtp.return_value
                self.assertTrue(pkg.send_email("text", "subject"))
                pkg.input_timeout.assert_called_with("email: ")
                pkg.input_timeout.assert_any_call("SMTP server (e.g. smtp.gmail.com): ")
                pkg.getpass.getpass.assert_called_once()
                pkg.store_pwd_in_keyring.assert_called_once()
                self.assertEqual(pkg.CONFIG.get("Email", "smtp_server"), "localhost")
                self.assertEqual(pkg.CONFIG.get("Email", "email"), "test@mail.com")
                context = server.__enter__.return_value
                context.login.assert_called_once_with("test@mail.com", "mypassword")
                context.send_message.assert_called_once()
                msg = context.send_message.call_args[0][0]
                # print(context.send_message.call_args, context.send_message.call_args[0])
                # print(dir(context.send_message.call_args))
                self.assertEqual(msg["Subject"], "subject")
                self.assertEqual(msg.get_content(), "text\n")
                self.assertEqual(msg["To"], 'test@mail.com')
                self.assertEqual(msg["From"], 'test@mail.com')
                self.assertEqual(len(captured.records), 1)
                self.assertTrue("Email sent" in captured.records[-1].getMessage())

        # email sending -- auth failure
        with self.assertLogs() as captured:
            with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
                server = mock_smtp.return_value
                context = server.__enter__.return_value
                context.login.side_effect = smtplib.SMTPAuthenticationError(0, "Login failed")
                self.assertFalse(pkg.send_email("text", "subject"))
                self.assertEqual(len(captured.records), 3)
                log = captured.records[-1]
                self.assertEqual(log.args[0], "test@mail.com")
                self.assertEqual(log.levelname, "ERROR")
                self.assertTrue("Authentication failed" in log.getMessage())
        # email sending -- other error
        with self.assertLogs() as captured:
            with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
                server = mock_smtp.return_value
                context = server.__enter__.return_value
                context.send_message.side_effect = smtplib.SMTPConnectError(0, "Error")
                self.assertFalse(pkg.send_email("text", "subject"))
                self.assertEqual(len(captured.records), 1)
                self.assertEqual(captured.records[-1].getMessage(), "Email sending failed, please check the configuration file")

    def test_query(self):
        url = f'{pkg.API_URL}search_query=cat:quant-ph&sortOrder=descending&max_results=10' \
               + '&start={start}'
        res = pkg._query(url)
        self.assertEqual(len(res), 10)

        with mock.patch('feedparser.parse') as mock_parse:
            mock_parse.side_effect = [
                {'bozo_exception': 'error', 'entries': []},  # error in parse
                {'feed': {'opensearch_totalresults': 0}, 'entries': []}, # ok no results
                {'feed': {'opensearch_totalresults': 2}, 'entries': []}, # error, there should be results
                {'feed': {'opensearch_totalresults': 0}, 'entries': []}, # ok no results
                {'feed': {'opensearch_totalresults': 2}, 'entries': []}, # error, there should be results
                {'feed': {'opensearch_totalresults': 2}, 'entries': []}, # error, there should be results
                {'feed': {'opensearch_totalresults': 2}, 'entries': []}, # error, there should be results
            ]

            with self.assertRaises(ValueError) as exc:
                pkg._query(url)
            self.assertEqual(exc.exception.args[0], "error")
            self.assertFalse(pkg._query(url)) # no results
            self.assertFalse(pkg._query(url)) # first trial fails, second trial no results
            with self.assertRaises(ValueError) as exc:
                pkg._query(url, max_trials=3)
            self.assertEqual(exc.exception.args[0], "Failed to retrieve results from API.")

    def test_api_query(self):
        now = datetime.now()
        with mock.patch("feedparser.parse") as mock_parse:
            parse1 = {"entries": [mock_feed_entry(now - timedelta(days=3))]*3}
            parse2 = {"entries": [mock_feed_entry(now - timedelta(days=1))]*50}
            parse3 = {"entries": [mock_feed_entry(now - timedelta(days=1))]*3}
            parse4 = {"entries": [], "feed": {"opensearch_totalresults": 3}}
            mock_parse.side_effect = [parse1, parse2, parse3] + [parse4]*10
            keywords = "%22quantum%22+OR+%22machine+learning%22"
            authors = "%22Jane+Doe%22+OR+%22Paul+Smith%22"
            args = [f"%28ti:%28{keywords}%29+OR+abs:%28{keywords}%29%29",
                    f"au:%28{authors}%29"]

            search_query = f"cat:%28quant-ph%29+AND+%28{'+OR+'.join(args)}%29"

            url = f'{pkg.API_URL}search_query={search_query}' \
                  f'&sortBy=submittedDate&sortOrder=descending&max_results=50' \
                  '&start={start}'
            res = pkg.api_query(now - timedelta(days=2))
            self.assertFalse(list(res))
            mock_parse.assert_called_with(url.format(start=0))

            res = pkg.api_query(now - timedelta(days=2))
            self.assertIsInstance(res, types.GeneratorType)
            self.assertEqual(res.send(None), parse2["entries"][0])
            mock_parse.assert_called_with(url.format(start=0))
            self.assertEqual(len(list(res)), 52)
            mock_parse.assert_called_with(url.format(start=50))

            # failure
            res = pkg.api_query(now - timedelta(days=2))
            with self.assertRaises(ValueError) as exc:
                res.send(None)
            self.assertEqual(exc.exception.args[0], "Failed to retrieve results from API.")

        pkg.CONFIG.set("General", "categories", "")
        with self.assertRaises(ValueError) as exc:
            list(pkg.api_query(now - timedelta(days=2)))
        self.assertEqual(exc.exception.args[0], "No category selected. Please edit the configuration file.")

        # only category, no filtering
        pkg.CONFIG.set("General", "categories", "quant-ph")
        pkg.CONFIG.set("General", "keywords", "")
        pkg.CONFIG.set("General", "authors", "")
        with mock.patch("feedparser.parse") as mock_parse:
            parse1 = {"entries": [{"updated_parsed": (now - timedelta(days=3)).timetuple()}]*3}
            mock_parse.return_value = parse1

            search_query = "cat:%28quant-ph%29"

            url = f'{pkg.API_URL}search_query={search_query}' \
                  f'&sortBy=submittedDate&sortOrder=descending&max_results=50' \
                  '&start={start}'
            res = pkg.api_query(now - timedelta(days=2))
            self.assertFalse(list(res))
            mock_parse.assert_called_with(url.format(start=0))

            pkg.CONFIG.set("General", "categories", "quant-ph, physics")
            search_query = "cat:%28quant-ph+OR+physics%29"

            url = f'{pkg.API_URL}search_query={search_query}' \
                  f'&sortBy=submittedDate&sortOrder=descending&max_results=50' \
                  '&start={start}'
            res = pkg.api_query(now - timedelta(days=2))
            self.assertFalse(list(res))
            mock_parse.assert_called_with(url.format(start=0))

    @mock.patch("arxiv_update_cli._query", mock.Mock())
    def test_api_general_query(self):

        url = f'{pkg.API_URL}search_query=&id_list=&sortBy=lastUpdatedDate&sortOrder=descending&max_results=200' \
               '&start={start}'
        # no result
        pkg._query.return_value = []
        res = pkg.api_general_query()
        self.assertIsInstance(res, types.GeneratorType)
        self.assertFalse(len(list(res)))
        pkg._query.assert_called_once_with(url, 0, 1)

        start_date = datetime(2022, 4, 11)
        end_date = datetime(2022, 11, 30)
        entries = [mock_feed_entry(start_date - timedelta(days=1)),
                   mock_feed_entry(start_date + timedelta(days=1)),
                   mock_feed_entry(end_date - timedelta(days=1)),
                   mock_feed_entry(end_date + timedelta(days=1))]

        # by: relevance
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(sort_by="relevance"))
        self.assertEqual(res, entries)
        ## max results
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_by="relevance", max_results=2))
        self.assertEqual(res, entries[:2])
        ## dates (ignored)
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(sort_by="relevance", start_date=start_date, end_date=end_date))
        self.assertEqual(res, entries)

        # by: lastUpdatedDate, order: descending
        entries.sort(key=lambda x: x["updated_parsed"], reverse=True)
        ## all
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query())
        self.assertEqual(res, entries)
        ## max results
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(max_results=2))
        self.assertEqual(res, entries[:2])
        ## start_date
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(start_date=start_date))
        self.assertEqual(res, entries[:-1])
        ## end_date
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(end_date=end_date))
        self.assertEqual(res, entries[1:])
        ## start_date and end_date
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(start_date=start_date, end_date=end_date))
        self.assertEqual(res, entries[1:-1])
        ## start_date and end_date and max results
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(start_date=start_date, end_date=end_date, max_results=1))
        self.assertEqual(res, entries[1:2])
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(start_date=start_date, end_date=end_date, max_results=3))
        self.assertEqual(res, entries[1:-1])

        # by: submittedDate, order: descending
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(sort_by="submittedDate", start_date=start_date, end_date=end_date))
        self.assertEqual(res, entries[:-2])

        # by: lastUpdatedDate, order: ascending
        entries.sort(key=lambda x: x["updated_parsed"])
        ## all
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(sort_order="ascending"))
        self.assertEqual(res, entries)
        ## max results
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_order="ascending", max_results=2))
        self.assertEqual(res, entries[:2])
        ## start_date
        pkg._query.side_effect = [entries, []]
        res = list(pkg.api_general_query(sort_order="ascending", start_date=start_date))
        self.assertEqual(res, entries[1:])
        ## end_date
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_order="ascending", end_date=end_date))
        self.assertEqual(res, entries[:-1])
        ## start_date and end_date
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_order="ascending", start_date=start_date, end_date=end_date))
        self.assertEqual(res, entries[1:-1])
        ## start_date and end_date and max results
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_order="ascending", start_date=start_date, end_date=end_date, max_results=1))
        self.assertEqual(res, entries[1:2])
        pkg._query.side_effect = [entries]
        res = list(pkg.api_general_query(sort_order="ascending", start_date=start_date, end_date=end_date, max_results=3))
        self.assertEqual(res, entries[1:-1])

    def test_format_entry(self):
        entry = {  # minimum info
            "authors": [{'name': 'Jane Doe'}, {'name': 'Paul K. Smith'}],
            "title": "Title",
            "summary": "Ábstract.",
            "link": 'http://arxiv.org/abs/XXXX.XXXXX',
            "updated_parsed": datetime(2022, 1, 30).timetuple(),
        }
        entry2 = entry.copy()
        entry2.update({
            "arxiv_comment": "X pages, Y figures",
            "arxiv_journal_ref": "Journal, X, PP",
            "arxiv_doi": "DOI",
            "tags": [{'term': 'hep-lat'}, {'term': 'quant-ph'}]
        })
        entry3 = entry.copy()
        entry3["tags"] = [{'term': 'quant-ph'}]

        self.assertEqual(pkg.format_entry(entry, "id"), "XXXX.XXXXX")
        self.assertEqual(pkg.format_entry(entry, "title"), "2022-01-30 - Title - \033[36mhttp://arxiv.org/abs/XXXX.XXXXX\033[0m")
        res = pkg.format_entry(entry, "bibtex")
        print(res)
        self.assertTrue("@article{doe_title_2022" in res)
        self.assertTrue("year = {2022}" in res)
        self.assertTrue("@article{smith_title_2022" in pkg.format_bibtex("A title", ['Paul K. Smith', 'Jane Doe'],
                                                                       'http://arxiv.org/abs/XXXX.XXXXX',
                                                                       datetime(2022, 1, 30)))

        res = pkg.format_entry(entry, "condensed")
        self.assertEqual(len(res.strip().splitlines()), 3)
        self.assertTrue("2022-01-30" in res)
        self.assertFalse("Ábstract" in res)
        self.assertTrue("Title" in res)
        self.assertTrue("Jane Doe" in res)
        self.assertTrue("Paul K. Smith" in res)
        self.assertTrue("http://arxiv.org/abs/XXXX.XXXXX" in res)
        self.assertEqual(res, pkg.format_entry(entry2, "condensed"))

        res = pkg.format_entry(entry, "full")
        res2 = pkg.format_entry(entry2, "full")
        res3 = pkg.format_entry(entry3, "full")
        self.assertNotEqual(res, res2)
        self.assertFalse("Comment" in res)
        self.assertTrue("Comment" in res2)
        self.assertTrue("DOI" in res2)
        self.assertTrue("Subjects:" in res2)
        self.assertTrue("hep-lat" in res2)
        self.assertTrue("quant-ph" in res2)
        self.assertTrue("Subject:" in res3)
        self.assertFalse("hep-lat" in res3)
        self.assertTrue("quant-ph" in res3)
        self.assertTrue("Journal reference" in res2)
        self.assertTrue("Journal, X, PP" in res2)
        self.assertTrue("X pages, Y figures" in res2)
        self.assertEqual(pkg.format_entry(entry, None), res)
