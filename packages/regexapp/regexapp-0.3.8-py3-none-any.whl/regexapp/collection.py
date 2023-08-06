"""Module containing the logic for the collection of pattern."""

import re
import yaml
import string
from textwrap import dedent
from pathlib import Path, PurePath
from copy import copy

from regexapp.exceptions import EscapePatternError
from regexapp.exceptions import PatternReferenceError
from regexapp.exceptions import TextPatternError
from regexapp.exceptions import ElementPatternError
from regexapp.exceptions import LinePatternError
from regexapp.exceptions import MultilinePatternError
from regexapp.exceptions import PatternBuilderError

import logging
logger = logging.getLogger(__file__)


def validate_pattern(pattern, flags=0, exception_cls=None):
    """validate a pattern

    Parameters
    ----------
    pattern (str): a pattern.
    exception_cls (Exception): an exception class.  Default is None.
    """
    exception_cls = exception_cls or Exception
    try:
        re.compile(pattern, flags=flags)
    except Exception as ex:
        msg = '{} - {}'.format(type(ex).__name__, ex)
        raise exception_cls(msg)


def do_soft_regex_escape(pattern, is_validated=True):
    """Escape special characters in a string.  This method will help
    consistency pattern during invoking re.escape on different Python version.

    Parameters
    ----------
    pattern (str): a pattern.
    is_validated (bool): need to validate pattern after escape.  Default is False.

    Returns
    -------
    str: return a new pattern if there is special characters that needs to escape.

    Raises
    ------
    EscapePatternError: if error during validating pattern.
    """
    pattern = str(pattern)
    chk1, chk2 = string.punctuation + ' ', '^$.?*+|{}[]()'
    result = []
    for char in pattern:
        echar = re.escape(char)
        if char in chk1:
            result.append(echar if char in chk2 else char)
        else:
            result.append(echar)
    new_pattern = ''.join(result)
    is_validated and validate_pattern(new_pattern, exception_cls=EscapePatternError)
    return new_pattern


class VarCls:
    """Use to store variable for pattern

    Attribute
    ---------
    name (str): variable name.  Default is empty.
    pattern (str): a regex pattern.  Default is empty.
    option (str): an option for value assignment.  Default is empty.

    Properties
    ----------
    is_empty -> bool
    value -> str
    var_name -> str
    """
    def __init__(self, name='', pattern='', option=''):
        self.name = str(name).strip()
        self.pattern = str(pattern)
        self.option = ','.join(re.split(r'\s*_\s*', str(option).title()))
        self.option = self.option.replace(' ', '')

    @property
    def is_empty(self):
        return self.name == ''

    @property
    def value(self):
        if self.option:
            self.option = ','.join(re.split(r'\s*_\s*', str(self.option).title()))
            self.option = self.option.replace(' ', '')
            fmt = 'Value {} {} ({})'
            value = fmt.format(self.option, self.name, self.pattern)
        else:
            fmt = 'Value {} ({})'
            value = fmt.format(self.name, self.pattern)
        return value

    @property
    def var_name(self):
        result = '${%s}' % self.name
        return result


class PatternReference(dict):
    """Use to load regular expression pattern from system_references.yaml
    or/and user_references.yaml

    Attribute
    ---------
    sys_ref_loc (str): a system references file name.
    user_ref_loc (str): a user references file name.

    Methods
    -------
    load_reference(filename) -> None
    PatternReference.get_pattern_layout(name) -> str
    is_valid_format(name, value) -> bool
    is_violated(dict_obj) -> bool
    test(self, content) -> bool

    Raises
    ------
    PatternReferenceError: raise exception if filename doesn't exist or
            an invalid format
    """

    # regexp pattern - from system references
    sys_ref_loc = str(PurePath(Path(__file__).parent, 'system_references.yaml'))
    # regex patterns - from user references
    user_ref_loc = str(PurePath(Path.home(), '.regexapp', 'user_references.yaml'))

    def __init__(self):
        super().__init__()
        self.load_reference(self.sys_ref_loc)
        self.load_reference(self.user_ref_loc)
        self.test_result = ''
        self.violated_format = ''

    def load_reference(self, filename):
        """Load reference from YAML references file.
        Parameters
        ----------
        filename (str): a file name.

        Returns
        -------
        None: no return

        Raises
        ------
        PatternReferenceError: raise exception if filename doesn't exist or
                an invalid format
        """
        node = Path(filename)
        if not node.exists():
            if filename == self.sys_ref_loc:
                msg = '{} is NOT FOUND.'.format(filename)
                raise PatternReferenceError(msg)
            else:
                # fmt = '%s is NOT existed.  CANT load reference.'
                # logger.warning(fmt, filename)
                return

        try:
            with node.open() as stream:
                yaml_obj = yaml.load(stream, Loader=yaml.SafeLoader)

                if not yaml_obj:
                    return

                if not isinstance(yaml_obj, dict):
                    fmt = '{} must be structure as dictionary.'
                    raise PatternReferenceError(fmt.format(filename))

                for key, value in yaml_obj.items():
                    if key not in self:
                        self[key] = value
                    else:
                        if key == 'datetime':
                            self[key] = value
                        else:
                            fmt = ('%r key is already existed.  '
                                   'Wont update %r data to key.')
                            logger.warning(fmt, key, value)
        except Exception as ex:
            msg = '{} - {}'.format(type(ex).__name__, ex)
            raise PatternReferenceError(msg)

    @classmethod
    def get_pattern_layout(cls, name):
        layout1 = """
            name_placeholder:
              ##################################################################
              # double back flash must be used in a value of pattern if needed
              # positive test and/or negative test is/are optional
              ##################################################################
              group: "replace_me"
              description: "replace_me"
              pattern: "replace_me"
              # positive test:
              #   change this positive test name: "replace_me -> (string or list of string)"
              # negative test:
              #   change this negative test name: "replace_me -> (string or list of string)"
        """
        layout2 = """
            name_placeholder:
              ##################################################################
              # double back flash must be used in a value of format if needed
              # positive test and/or negative test is/are optional
              ##################################################################
              group: "replace_me"
              description: "replace_me"
              format: "replace_me"
              # format1: "replace_me"
              # format2: "replace_me"
              # formatn: "replace_me"
              # positive test:
              #   change this positive test name: "replace_me -> (string or list of string)"
              # negative test:
              #   change this negative test name: "replace_me -> (string or list of string)"
        """
        layout1, layout2 = dedent(layout1).strip(), dedent(layout2).strip()
        return layout2 if 'datetime' in name else layout1

    def is_valid_format(self, name, value):
        """Check if name and value are valid

        Parameters
        ----------
        name (str): a name of reference
        value (dict): a value of reference

        Returns
        -------
        bool: True if a reference is valid.
        """
        fmt1 = 'value of "{}" MUST be a dictionary'
        fmt2 = 'value of "{}" MUST have "group" key'
        fmt3 = 'value of "{}" MUST have "description" key'
        fmt4 = 'value of "positive test" of "{}" MUST be a dictionary'
        fmt5 = 'value of "negative test" of "{}" MUST be a dictionary'
        fmt6 = ('value of "{}" (i.e datetime reference) '
                'MUST have "format" or "format#" key')
        fmt7 = 'value of "{}" MUST have "pattern" key'

        if not isinstance(value, dict):
            self.violated_format = fmt1.format(name)
            return False

        if 'group' not in value:
            self.violated_format = fmt2.format(name)
            return False

        if 'description' not in value:
            self.violated_format = fmt3.format(name)
            return False

        if 'positive test' in value:
            pos_test_value = value.get('positive test')
            if not isinstance(pos_test_value, dict):
                self.violated_format = fmt4.format(name)
                return False

        if 'negative test' in value:
            neg_test_value = value.get('positive test')
            if not isinstance(neg_test_value, dict):
                self.violated_format = fmt5.format(name)
                return False

        if 'datetime' in name:
            for key in value:
                if 'format' in key:
                    return True
            self.violated_format = fmt6.format(name)
            return False
        else:
            if 'pattern' in value:
                return True
            else:
                self.violated_format = fmt7.format(name)
                return False

    def is_violated(self, dict_obj):
        """Check if new pattern reference doesn't violate with system reference

        Parameters
        ----------
        dict_obj (dict): a dict object.

        Returns
        -------
        bool: True there is a violation.
        """
        sys_ref = yaml.load(open(self.sys_ref_loc), Loader=yaml.SafeLoader)
        fmt = '{} is ALREADY existed in system_references.yaml'
        for name in dict_obj:
            if 'datetime' not in name:
                if name in sys_ref:
                    self.violated_format = fmt.format(name)
                    return True
        return False

    def test(self, content):
        """test pattern reference.
        Parameters
        ----------
        content (str): a content of YAML format.

        Returns
        -------
        bool: True if content is a valid format

        Raises
        ------
        PatternReferenceError: raise exception if a content is
                an invalid format or violate system_references.yaml
        """

        try:
            yaml_obj = yaml.load(content, Loader=yaml.SafeLoader)
        except Exception as ex:
            msg = '{} - {}'.format(type(ex).__name__, ex)
            raise PatternReferenceError(msg)

        if not yaml_obj:
            logger.warning('CANT test an empty content')
            self.test_result = 'not_tested'
            return True

        if not isinstance(yaml_obj, dict):
            msg = 'content must be structure of dictionary.'
            raise PatternReferenceError(msg)

        for name, value in yaml_obj.items():
            if not self.is_valid_format(name, value):
                raise PatternReferenceError(self.violated_format)

        if self.is_violated(yaml_obj):
            raise PatternReferenceError(self.violated_format)

        self.test_result = 'tested'
        return True


class SymbolCls(dict):
    """Use to load symbols.yaml

    Attribute
    ---------
    filename (str): a system references file name.
    """

    filename = str(PurePath(Path(__file__).parent, 'symbols.yaml'))

    def __init__(self):
        stream = open(self.filename)
        obj = yaml.load(stream, Loader=yaml.SafeLoader)
        super().__init__(obj)


REF = PatternReference()

SYMBOL = SymbolCls()


class TextPattern(str):
    """Use to convert text data to regex pattern

    Attributes
    ----------
    text (str): a text.
    as_is (bool): keeping text an AS-IS pattern.

    Properties
    ----------
    is_empty (bool): check if a pattern matches empty string.
    is_empty_or_whitespace (bool): check if a pattern matches empty string or whitespace
    is_whitespace (bool): check if a pattern matches whitespace

    Methods
    -------
    TextPattern.get_pattern(text) -> str
    lstrip(chars=None) -> TextPattern
    rstrip(chars=None) -> TextPattern
    strip(chars=None) -> TextPattern
    add(other, as_is=True) -> TextPattern
    concatenate(*other, as_is=True) -> TextPattern

    Raises
    ------
    TextPatternError: raise an exception if pattern is invalid.
    """
    def __new__(cls, text, as_is=False):
        data = str(text)

        if as_is:
            return str.__new__(cls, data)

        if data:
            text_pattern = cls.get_pattern(data)
        else:
            text_pattern = ''
        return str.__new__(cls, text_pattern)

    def __init__(self, text, as_is=False):
        self.text = text
        self.as_is = as_is

    def __add__(self, other):
        result = super().__add__(other)
        result_pat = TextPattern(result, as_is=True)
        return result_pat

    def __radd__(self, other):
        if isinstance(other, TextPattern):
            return other.__add__(self)
        else:
            other_pat = TextPattern(other, as_is=True)
            return other_pat.__add__(self)

    @property
    def is_empty(self):
        if self == '':
            return True
        else:
            result = re.match(str(self), '')
            return bool(result)

    @property
    def is_empty_or_whitespace(self):
        is_empty = self.is_empty
        is_ws = bool(re.match(str(self), ' '))
        return is_empty or is_ws

    @property
    def is_whitespace(self):
        is_ws = bool(re.match(str(self), ' '))
        return is_ws

    @classmethod
    def get_pattern(cls, text):
        """convert data to regex pattern

        Parameters
        ----------
        text (str): a text

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        TextPatternError: raise an exception if pattern is invalid.
        """
        start = 0
        result = []
        for item in re.finditer(r'\s+', text):
            before_matched = text[start: item.start()]
            before_matched and result.append(do_soft_regex_escape(before_matched))
            matched = item.group()
            total = len(matched)
            lst = list(matched)
            is_space = lst[0] == ' ' and len(set(lst)) == 1
            is_space and result.append(' ' if total == 1 else ' +')
            not is_space and result.append(r'\s' if total == 1 else r'\s+')
            start = item.end()
        else:
            if result:
                after_matched = text[start:]
                after_matched and result.append(do_soft_regex_escape(after_matched))
            else:
                result.append(do_soft_regex_escape(text))

        text_pattern = ''.join(result)

        validate_pattern(text_pattern, exception_cls=TextPatternError)
        return text_pattern

    def lstrip(self, chars=None):
        """Return a copy of the TextPattern with leading whitespace removed.

        Parameters
        ----------
        chars (None, str): If chars is given and not None,
                remove characters in chars instead.

        Returns
        -------
        TextPattern: a new TextPattern with leading whitespace removed.

        """
        new_text = self.text.lstrip() if chars is None else self.text.lstrip(chars)
        pattern = TextPattern(new_text)
        return pattern

    def rstrip(self, chars=None):
        """Return a copy of the TextPattern with trailing whitespace removed.

        Parameters
        ----------
        chars (None, str): If chars is given and not None,
                remove characters in chars instead.

        Returns
        -------
        TextPattern: a new TextPattern with trailing whitespace removed.

        """
        new_text = self.text.rstrip() if chars is None else self.text.rstrip(chars)
        pattern = TextPattern(new_text)
        return pattern

    def strip(self, chars=None):
        """Return a copy of the TextPattern with leading and
        trailing whitespace removed.

        Parameters
        ----------
        chars (None, str): If chars is given and not None,
                remove characters in chars instead.

        Returns
        -------
        TextPattern: a new TextPattern with leading and trailing whitespace removed.

        """
        new_text = self.text.strip() if chars is None else self.text.strip(chars)
        pattern = TextPattern(new_text)
        return pattern

    def add(self, other, as_is=True):
        """return a concatenated TextPattern.

        Parameters
        ----------
        other (str, TextElement): other
        as_is (bool): a flag to keep adding other AS-IS condition.

        Returns
        -------
        TextPattern: a concatenated TextPattern instance.
        """
        if isinstance(other, TextPattern):
            result = self + other
        else:
            if isinstance(other, (list, tuple)):
                result = self
                for item in other:
                    if isinstance(item, TextPattern):
                        result = result + item
                    else:
                        item_pat = TextPattern(str(item), as_is=as_is)
                        result = result + item_pat
            else:
                other_pat = TextPattern(str(other), as_is=as_is)
                result = self + other_pat

        return result

    def concatenate(self, *other, as_is=True):
        """return a concatenated TextPattern.

        Parameters
        ----------
        other (tuple): other
        as_is (bool): a flag to keep adding other AS-IS condition.

        Returns
        -------
        TextPattern: a concatenated TextPattern instance.
        """
        result = self
        for item in other:
            result = result.add(item, as_is=as_is)
        return result


class ElementPattern(str):
    """Use to convert element data to regex pattern

    Attributes
    ----------
    variable (VarCls): a regex variable.
    or_empty (bool): a flag if pattern is expecting a zero match, i.e. empty.
            Default is False.

    Parameters
    ----------
    text (str): a text.
    as_is (bool): keeping text an AS-IS pattern.

    Methods
    -------
    ElementPattern.get_pattern(data) -> str
    ElementPattern.build_pattern(keyword, params) -> str
    ElementPattern.build_custom_pattern(keyword, params) -> bool, str
    ElementPattern.build_datetime_pattern(keyword, params) -> bool, str
    ElementPattern.build_choice_pattern(keyword, params) -> bool, str
    ElementPattern.build_data_pattern(keyword, params) -> bool, str
    ElementPattern.build_start_pattern(keyword, params) -> bool, str
    ElementPattern.build_end_pattern(keyword, params) -> bool, str
    ElementPattern.build_raw_pattern(keyword, params) -> bool, str
    ElementPattern.build_default_pattern(keyword, params) -> bool, str
    ElementPattern.join_list(lst) -> str
    ElementPattern.add_var_name(pattern, name='') -> str
    ElementPattern.add_word_bound(pattern, word_bound='', added_parentheses=True) -> str
    ElementPattern.add_start_of_string(pattern, head='') -> str
    ElementPattern.add_end_of_string(pattern, tail='') -> str
    ElementPattern.add_repetition(lst, repetition='') -> list
    ElementPattern.add_occurrence(lst, occurrence='') -> list
    ElementPattern.add_case_occurrence(lst, first, last, is_phrase) -> bool
    ElementPattern.is_singular_pattern(pattern) -> bool
    remove_head_of_string() -> ElementPattern
    remove_tail_of_string() -> ElementPattern

    Raises
    ------
    ElementPatternError: raise an exception if pattern is invalid.
    """
    # patterns
    word_bound_pattern = r'word_bound(_left|_right|_raw)?$'
    head_pattern = r'head(_raw|((_just)?_(whitespaces?|ws|spaces?)(_plus)?))?$'
    tail_pattern = r'tail(_raw|((_just)?_(whitespaces?|ws|spaces?)(_plus)?))?$'
    repetition_pattern = r'repetition_\d*(_\d*)?$'
    occurrence_pattern = r'({})(?P<is_phrase>_(group|phrase))?_occurrences?$'.format(
        '|'.join([
            r'((?P<fda>\d+)_or_(?P<lda>\d+))',
            r'((?P<fdb>\d+)_or_(?P<ldb>more))',
            r'(at_(?P<fdc>least|most)_(?P<ldc>\d+))',
            r'(?P<fdd>\d+)'
        ])
    )
    meta_data_pattern = r'^meta_data_\w+'
    _variable = None

    def __new__(cls, text, as_is=False):
        cls._variable = VarCls()
        cls._or_empty = False
        cls._prepended_pattern = ''
        cls._appended_pattern = ''
        data = str(text)

        if as_is:
            return str.__new__(cls, data)

        if data:
            pattern = cls.get_pattern(data)
        else:
            pattern = ''
        return str.__new__(cls, pattern)

    def __init__(self, text, as_is=False):
        self.text = text
        self.as_is = as_is
        self.variable = self._variable
        self.or_empty = self._or_empty
        self.prepended_pattern = self._prepended_pattern
        self.appended_pattern = self._appended_pattern

        # clear class variable after initialization
        self._variable = VarCls()
        self._or_empty = False
        self._prepended_pattern = ''
        self._appended_pattern = ''

    @classmethod
    def get_pattern(cls, text):
        """convert data to regex pattern

        Parameters
        ----------
        text (str): a text

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        ElementPatternError: raise an exception if pattern is invalid.
        """
        sep_pat = r'(?P<keyword>\w+)[(](?P<params>.*)[)]$'
        match = re.match(sep_pat, text.strip())
        if match:
            keyword = match.group('keyword')
            params = match.group('params').strip()
            pattern = cls.build_pattern(keyword, params)
        else:
            pattern = do_soft_regex_escape(text)

        validate_pattern(pattern, exception_cls=ElementPatternError)
        return pattern

    @classmethod
    def build_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        is_built, raw_pattern = cls.build_raw_pattern(keyword, params)
        if is_built:
            return raw_pattern

        is_built, start_pattern = cls.build_start_pattern(keyword, params)
        if is_built:
            return start_pattern

        is_built, end_pattern = cls.build_end_pattern(keyword, params)
        if is_built:
            return end_pattern

        is_built, symbol_pattern = cls.build_symbol_pattern(keyword, params)
        if is_built:
            return symbol_pattern

        is_built, datetime_pattern = cls.build_datetime_pattern(keyword, params)
        if is_built:
            return datetime_pattern

        is_built, choice_pattern = cls.build_choice_pattern(keyword, params)
        if is_built:
            return choice_pattern

        is_built, data_pattern = cls.build_data_pattern(keyword, params)
        if is_built:
            return data_pattern

        is_built, custom_pattern = cls.build_custom_pattern(keyword, params)
        if is_built:
            return custom_pattern

        _, default_pattern = cls.build_default_pattern(keyword, params)
        return default_pattern

    @classmethod
    def build_custom_pattern(cls, keyword, params):
        """build a custom pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        if keyword not in REF:
            return False, ''

        arguments = re.split(r' *, *', params) if params else []

        lst = [REF.get(keyword).get('pattern')]

        name, vpat = '', r'var_(?P<name>\w+)$'
        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False
        word_bound = ''
        head = ''
        tail = ''
        is_repeated = False
        is_occurrence = False

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            elif re.match(cls.word_bound_pattern, arg):
                if arg == 'word_bound_raw':
                    'word_bound' not in lst and lst.append('word_bound')
                else:
                    word_bound = arg
            elif re.match(cls.head_pattern, arg):
                if arg == 'head_raw':
                    'head' not in lst and lst.append('head')
                else:
                    head = arg
            elif re.match(cls.tail_pattern, arg):
                if arg == 'tail_raw':
                    'tail' not in lst and lst.append('tail')
                else:
                    tail = arg
            elif re.match(cls.repetition_pattern, arg):
                if not is_repeated or not is_occurrence:
                    lst = cls.add_repetition(lst, repetition=arg)
                    is_repeated = True
            elif re.match(cls.occurrence_pattern, arg):
                if not is_repeated or not is_occurrence:
                    lst = cls.add_occurrence(lst, occurrence=arg)
                    is_occurrence = True
            elif re.match(cls.meta_data_pattern, arg):
                if arg == 'meta_data_raw':
                    'meta_data' not in lst and lst.append('meta_data')
                else:
                    cls._variable.option = arg.lstrip('meta_data_')
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                        cls._or_empty = is_empty
                    else:
                        if case in REF:
                            pat = REF.get(case).get('pattern')
                            pat not in lst and lst.append(pat)
                        else:
                            pat = case
                            pat not in lst and lst.append(pat)
                else:
                    pat = do_soft_regex_escape(arg)
                    pat not in lst and lst.append(pat)

        is_empty and lst.append('')
        is_multiple = len(lst) > 1
        pattern = cls.join_list(lst)
        pattern = cls.add_word_bound(
            pattern, word_bound=word_bound, added_parentheses=is_multiple
        )
        pattern = cls.add_var_name(pattern, name=name)
        pattern = cls.add_head_of_string(pattern, head=head)
        pattern = cls.add_tail_of_string(pattern, tail=tail)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_symbol_pattern(cls, keyword, params):
        """build a symbol over given keyword, params

        Parameters
        ----------
        keyword (str): a symbol keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        if keyword != 'symbol' or not params.strip():
            return False, ''

        arguments = re.split(r' *, *', params) if params else []
        symbol_name, removed_items = '', []
        for arg in arguments:
            if arg.startswith('name='):
                symbol_name = arg[5:]
                removed_items.append(arg)

        if not removed_items:
            return False, ''
        else:
            for item in removed_items:
                item in arguments and arguments.remove(item)

        val = SYMBOL.get(symbol_name, do_soft_regex_escape(symbol_name))
        lst = [val]

        name, vpat = '', r'var_(?P<name>\w+)$'
        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False
        word_bound = ''
        head = ''
        tail = ''
        is_repeated = False
        is_occurrence = False

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            elif re.match(cls.word_bound_pattern, arg):
                if arg == 'word_bound_raw':
                    'word_bound' not in lst and lst.append('word_bound')
                else:
                    word_bound = arg
            elif re.match(cls.head_pattern, arg):
                if arg == 'head_raw':
                    'head' not in lst and lst.append('head')
                else:
                    head = arg
            elif re.match(cls.tail_pattern, arg):
                if arg == 'tail_raw':
                    'tail' not in lst and lst.append('tail')
                else:
                    tail = arg
            elif re.match(cls.repetition_pattern, arg):
                if not is_repeated or not is_occurrence:
                    lst = cls.add_repetition(lst, repetition=arg)
                    is_repeated = True
            elif re.match(cls.occurrence_pattern, arg):
                if not is_repeated or not is_occurrence:
                    lst = cls.add_occurrence(lst, occurrence=arg)
                    is_occurrence = True
            elif re.match(cls.meta_data_pattern, arg):
                if arg == 'meta_data_raw':
                    'meta_data' not in lst and lst.append('meta_data')
                else:
                    cls._variable.option = arg.lstrip('meta_data_')
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                        cls._or_empty = is_empty
                    else:
                        if case in REF:
                            pat = REF.get(case).get('pattern')
                            pat not in lst and lst.append(pat)
                        else:
                            pat = case
                            pat not in lst and lst.append(pat)
                else:
                    pat = do_soft_regex_escape(arg)
                    pat not in lst and lst.append(pat)

        is_empty and lst.append('')
        is_multiple = len(lst) > 1
        pattern = cls.join_list(lst)
        pattern = cls.add_word_bound(
            pattern, word_bound=word_bound, added_parentheses=is_multiple
        )
        pattern = cls.add_var_name(pattern, name=name)
        pattern = cls.add_head_of_string(pattern, head=head)
        pattern = cls.add_tail_of_string(pattern, tail=tail)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_datetime_pattern(cls, keyword, params):
        """build a datetime pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        if keyword not in REF:
            return False, ''

        node = REF.get(keyword)
        fmt_lst = [key for key in node if key.startswith('format')]
        if not fmt_lst:
            return False, ''

        arguments = re.split(r' *, *', params) if params else []
        lst = []
        name, vpat = '', r'var_(?P<name>\w+)$'
        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            elif arg.startswith('format'):
                pat = node.get(arg)
                pat not in lst and lst.append(pat)
            # else:
            #     pat = arg
            #     pat not in lst and lst.append(pat)
        if not lst:
            lst.append(node.get('format'))

        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False
        word_bound = ''
        head = ''
        tail = ''

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match or arg.startswith('format'):
                continue
            elif re.match(cls.word_bound_pattern, arg):
                if arg == 'word_bound_raw':
                    'word_bound' not in lst and lst.append('word_bound')
                else:
                    word_bound = arg
            elif re.match(cls.head_pattern, arg):
                if arg == 'head_raw':
                    'head' not in lst and lst.append('head')
                else:
                    head = arg
            elif re.match(cls.tail_pattern, arg):
                if arg == 'tail_raw':
                    'tail' not in lst and lst.append('tail')
                else:
                    tail = arg
            elif re.match(cls.meta_data_pattern, arg):
                if arg == 'meta_data_raw':
                    'meta_data' not in lst and lst.append('meta_data')
                else:
                    cls._variable.option = arg.lstrip('meta_data_')
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                        cls._or_empty = is_empty
                    else:
                        if case in REF:
                            pat = REF.get(case).get('pattern')
                            pat not in lst and lst.append(pat)
                        else:
                            pat = case
                            pat not in lst and lst.append(pat)
                else:
                    pat = do_soft_regex_escape(arg)
                    pat not in lst and lst.append(pat)

        is_empty and lst.append('')
        pattern = cls.join_list(lst)
        pattern = cls.add_word_bound(pattern, word_bound=word_bound)
        pattern = cls.add_var_name(pattern, name=name)
        pattern = cls.add_head_of_string(pattern, head=head)
        pattern = cls.add_tail_of_string(pattern, tail=tail)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_choice_pattern(cls, keyword, params):
        """build a choice pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if keyword != 'choice':
            return False, ''

        arguments = re.split(r' *, *', params) if params else []
        lst = []

        name, vpat = '', r'var_(?P<name>\w+)$'
        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False
        word_bound = ''
        head = ''
        tail = ''

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            elif re.match(cls.word_bound_pattern, arg):
                if arg == 'word_bound_raw':
                    'word_bound' not in lst and lst.append('word_bound')
                else:
                    word_bound = arg
            elif re.match(cls.head_pattern, arg):
                if arg == 'head_raw':
                    'head' not in lst and lst.append('head')
                else:
                    head = arg
            elif re.match(cls.tail_pattern, arg):
                if arg == 'tail_raw':
                    'tail' not in lst and lst.append('tail')
                else:
                    tail = arg
            elif re.match(cls.meta_data_pattern, arg):
                if arg == 'meta_data_raw':
                    'meta_data' not in lst and lst.append('meta_data')
                else:
                    cls._variable.option = arg.lstrip('meta_data_')
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                        cls._or_empty = is_empty
                    else:
                        if case in REF:
                            pat = REF.get(case).get('pattern')
                            pat not in lst and lst.append(pat)
                        else:
                            pat = case
                            pat not in lst and lst.append(pat)
                else:
                    pat = do_soft_regex_escape(arg)
                    pat not in lst and lst.append(pat)

        is_empty and lst.append('')
        pattern = cls.join_list(lst)
        pattern = cls.add_word_bound(pattern, word_bound=word_bound)
        pattern = cls.add_var_name(pattern, name=name)
        pattern = cls.add_head_of_string(pattern, head=head)
        pattern = cls.add_tail_of_string(pattern, tail=tail)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_data_pattern(cls, keyword, params):
        """build a data pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if keyword != 'data':
            return False, ''

        arguments = re.split(r' *, *', params) if params else []
        lst = []

        name, vpat = '', r'var_(?P<name>\w+)$'
        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False
        word_bound = ''
        head = ''
        tail = ''

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            elif re.match(cls.word_bound_pattern, arg):
                if arg == 'word_bound_raw':
                    'word_bound' not in lst and lst.append('word_bound')
                else:
                    word_bound = arg
            elif re.match(cls.head_pattern, arg):
                if arg == 'head_raw':
                    'head' not in lst and lst.append('head')
                else:
                    head = arg
            elif re.match(cls.tail_pattern, arg):
                if arg == 'tail_raw':
                    'tail' not in lst and lst.append('tail')
                else:
                    tail = arg
            elif re.match(cls.meta_data_pattern, arg):
                if arg == 'meta_data_raw':
                    'meta_data' not in lst and lst.append('meta_data')
                else:
                    cls._variable.option = arg.lstrip('meta_data_')
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                        cls._or_empty = is_empty
                    else:
                        if case in REF:
                            pat = REF.get(case).get('pattern')
                            pat not in lst and lst.append(pat)
                        else:
                            pat = case
                            pat not in lst and lst.append(pat)
                else:
                    pat = do_soft_regex_escape(arg)
                    pat not in lst and lst.append(pat)

        is_empty and lst.append('')
        pattern = cls.join_list(lst)
        pattern = cls.add_word_bound(pattern, word_bound=word_bound)
        pattern = cls.add_var_name(pattern, name=name)
        pattern = cls.add_head_of_string(pattern, head=head)
        pattern = cls.add_tail_of_string(pattern, tail=tail)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_start_pattern(cls, keyword, params):
        """build a start pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if keyword != 'start':
            return False, ''

        table = dict(space=r'^ *', spaces=r'^ +', space_plus=r'^ +',
                     ws=r'^\s*', ws_plus=r'^\s+',
                     whitespace=r'^\s*', whitespaces=r'^\s+',
                     whitespace_plus=r'^\s+')
        pat = table.get(params, r'^')
        return True, pat

    @classmethod
    def build_end_pattern(cls, keyword, params):
        """build an end pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if keyword != 'end':
            return False, ''

        table = dict(space=r' *$', spaces=r' +$', space_plus=r' +$',
                     ws=r'\s*$', ws_plus=r'\s+$',
                     whitespace=r'\s*$', whitespaces=r'\s+$',
                     whitespace_plus=r'\s+$')
        pat = table.get(params, r'$')
        return True, pat

    @classmethod
    def build_raw_pattern(cls, keyword, params):
        """build a raw data pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if not params.startswith('raw>>>'):
            return False, ''
        params = re.sub(r'raw>+', '', params, count=1)
        new_params = do_soft_regex_escape(params)
        pattern = r'{}\({}\)'.format(keyword, new_params)
        return True, pattern

    @classmethod
    def build_default_pattern(cls, keyword, params):
        """build a default pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        pattern = do_soft_regex_escape('{}({})'.format(keyword, params))
        return True, pattern

    @classmethod
    def join_list(cls, lst):
        """join item of list

        Parameters
        ----------
        lst (list): list of pattern

        Returns
        -------
        str: a string data.
        """
        new_lst = []
        has_ws = False
        if len(lst) > 1:
            for item in lst:
                if ' ' in item or r'\s' in item:
                    has_ws = True
                    if item.startswith('(') and item.endswith(')'):
                        v = item
                    else:
                        if re.match(r' ([?+*]+|([{][0-9,]+[}]))$', item):
                            v = item
                        else:
                            v = '({})'.format(item)
                else:
                    v = item
                v not in new_lst and new_lst.append(v)
        else:
            new_lst = lst

        result = '|'.join(new_lst)

        has_empty = bool([True for i in new_lst if i == ''])
        if has_empty or len(new_lst) > 1 and has_ws:
            result = '({})'.format(result)

        return result

    @classmethod
    def add_var_name(cls, pattern, name=''):
        """add var name to regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        name (str): a regex variable name

        Returns
        -------
        str: new pattern with variable name.
        """
        if name:
            cls._variable.name = name
            cls._variable.pattern = pattern
            if pattern.startswith('(') and pattern.endswith(')'):
                sub_pat = pattern[1:-1]
                if pattern.endswith('|)'):
                    new_pattern = '(?P<{}>{})'.format(name, sub_pat)
                else:
                    try:
                        re.compile(sub_pat)
                        cls._variable.pattern = sub_pat
                        new_pattern = '(?P<{}>{})'.format(name, sub_pat)
                    except Exception as ex:     # noqa
                        new_pattern = '(?P<{}>{})'.format(name, pattern)
            else:
                new_pattern = '(?P<{}>{})'.format(name, pattern)
            return new_pattern
        return pattern

    @classmethod
    def add_word_bound(cls, pattern, word_bound='', added_parentheses=True):
        """add word bound i.e \\b to regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        word_bound (str): word bound case.  Default is empty.
                value of word_bound can be word_bound, word_bound_left,
                or word_bound_right
        added_parentheses (bool): always add parentheses to pattern.  Default is True.

        Returns
        -------
        str: new pattern with enclosing word bound pattern if it is required.
        """
        if not word_bound:
            return pattern

        has_ws = ' ' in pattern or r'\s' in pattern
        new_pattern = '({})'.format(pattern) if has_ws else pattern
        if added_parentheses:
            if not new_pattern.startswith('(') or not new_pattern.endswith(')'):
                new_pattern = '({})'.format(new_pattern)

        if word_bound == 'word_bound_left':
            new_pattern = r'\b{}'.format(new_pattern)
        elif word_bound == 'word_bound_right':
            new_pattern = r'{}\b'.format(new_pattern)
        else:
            new_pattern = r'\b{}\b'.format(new_pattern)
        return new_pattern

    @classmethod
    def add_head_of_string(cls, pattern, head=''):
        """prepend start of string i.e ^ or ^\\s* or ^\\s+ or ^ * or ^ + regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        head (str): start of string case.  Default is empty.

        Returns
        -------
        str: new pattern with start of string pattern
        """
        if head:
            case1, case2 = r'^\s*', r'^\s+'
            case3, case4 = r'^ *', r'^ +'
            case5 = r'^'

            case6, case7 = r'\s*', r'\s+'
            case8, case9 = r' *', r' +'

            case10, case11 = r'^\s*', r'^\s+'
            case12, case13 = r'\s*', r'\s+'

            if head == 'head_ws' and not pattern.startswith(case1):
                new_pattern = '{}{}'.format(case1, pattern)
                cls._prepended_pattern = case1
            elif head == 'head_ws_plus' and not pattern.startswith(case2):
                new_pattern = '{}{}'.format(case2, pattern)
                cls._prepended_pattern = case2
            elif head == 'head_space' and not pattern.startswith(case3):
                new_pattern = '{}{}'.format(case3, pattern)
                cls._prepended_pattern = case3
            elif head == 'head_space_plus' and not pattern.startswith(case4):
                new_pattern = '{}{}'.format(case4, pattern)
                cls._prepended_pattern = case4
            elif head == 'head_spaces' and not pattern.startswith(case4):
                new_pattern = '{}{}'.format(case4, pattern)
                cls._prepended_pattern = case4
            elif head == 'head' and not pattern.startswith(case5):
                new_pattern = '{}{}'.format(case5, pattern)
                cls._prepended_pattern = case5
            elif head == 'head_just_ws' and not pattern.startswith(case6):
                new_pattern = '{}{}'.format(case6, pattern)
                cls._prepended_pattern = case6
            elif head == 'head_just_ws_plus' and not pattern.startswith(case7):
                new_pattern = '{}{}'.format(case7, pattern)
                cls._prepended_pattern = case7
            elif head == 'head_just_space' and not pattern.startswith(case8):
                new_pattern = '{}{}'.format(case8, pattern)
                cls._prepended_pattern = case8
            elif head == 'head_just_space_plus' and not pattern.startswith(case9):
                new_pattern = '{}{}'.format(case9, pattern)
                cls._prepended_pattern = case9
            elif head == 'head_just_spaces' and not pattern.startswith(case9):
                new_pattern = '{}{}'.format(case9, pattern)
                cls._prepended_pattern = case9
            elif head == 'head_whitespace' and not pattern.startswith(case10):
                new_pattern = '{}{}'.format(case10, pattern)
                cls._prepended_pattern = case10
            elif head == 'head_whitespace_plus' and not pattern.startswith(case11):
                new_pattern = '{}{}'.format(case11, pattern)
                cls._prepended_pattern = case11
            elif head == 'head_whitespaces' and not pattern.startswith(case11):
                new_pattern = '{}{}'.format(case11, pattern)
                cls._prepended_pattern = case11
            elif head == 'head_just_whitespace' and not pattern.startswith(case12):
                new_pattern = '{}{}'.format(case12, pattern)
                cls._prepended_pattern = case12
            elif head == 'head_just_whitespace_plus' and not pattern.startswith(case13):
                new_pattern = '{}{}'.format(case13, pattern)
                cls._prepended_pattern = case13
            elif head == 'head_just_whitespaces' and not pattern.startswith(case13):
                new_pattern = '{}{}'.format(case13, pattern)
                cls._prepended_pattern = case13
            else:
                new_pattern = pattern
            return new_pattern
        return pattern

    @classmethod
    def add_tail_of_string(cls, pattern, tail=''):
        """append end of string i.e $ or \\s*$ or $\\s+$ or  *$ or  +$ regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        tail (str): end of string case.  Default is empty.

        Returns
        -------
        str: new pattern with end of string pattern
        """
        if tail:
            case1, case2 = r'\s*$', r'\s+$'
            case3, case4 = r' *$', r' +$'
            case5 = r'$'

            case6, case7 = r'\s*', r'\s+'
            case8, case9 = r' *', r' +'

            case10, case11 = r'\s*$', r'\s+$'
            case12, case13 = r'\s*', r'\s+'

            if tail == 'tail_ws' and not pattern.endswith(case1):
                new_pattern = '{}{}'.format(pattern, case1)
                cls._appended_pattern = case1
            elif tail == 'tail_ws_plus' and not pattern.endswith(case2):
                new_pattern = '{}{}'.format(pattern, case2)
                cls._appended_pattern = case2
            elif tail == 'tail_space' and not pattern.endswith(case3):
                new_pattern = '{}{}'.format(pattern, case3)
                cls._appended_pattern = case3
            elif tail == 'tail_space_plus' and not pattern.endswith(case4):
                new_pattern = '{}{}'.format(pattern, case4)
                cls._appended_pattern = case4
            elif tail == 'tail_spaces' and not pattern.endswith(case4):
                new_pattern = '{}{}'.format(pattern, case4)
                cls._appended_pattern = case4
            elif tail == 'tail' and not pattern.endswith(case5):
                new_pattern = '{}{}'.format(pattern, case5)
                cls._appended_pattern = case5
            elif tail == 'tail_just_ws' and not pattern.startswith(case6):
                new_pattern = '{}{}'.format(pattern, case6)
                cls._appended_pattern = case6
            elif tail == 'tail_just_ws_plus' and not pattern.startswith(case7):
                new_pattern = '{}{}'.format(pattern, case7)
                cls._appended_pattern = case7
            elif tail == 'tail_just_space' and not pattern.startswith(case8):
                new_pattern = '{}{}'.format(pattern, case8)
                cls._appended_pattern = case8
            elif tail == 'tail_just_space_plus' and not pattern.startswith(case9):
                new_pattern = '{}{}'.format(pattern, case9)
                cls._appended_pattern = case9
            elif tail == 'tail_just_spaces' and not pattern.startswith(case9):
                new_pattern = '{}{}'.format(pattern, case9)
                cls._appended_pattern = case9
            elif tail == 'tail_whitespace' and not pattern.startswith(case10):
                new_pattern = '{}{}'.format(pattern, case10)
                cls._appended_pattern = case10
            elif tail == 'tail_whitespace_plus' and not pattern.startswith(case11):
                new_pattern = '{}{}'.format(pattern, case11)
                cls._appended_pattern = case11
            elif tail == 'tail_whitespaces' and not pattern.startswith(case11):
                new_pattern = '{}{}'.format(pattern, case11)
                cls._appended_pattern = case11
            elif tail == 'tail_just_whitespace' and not pattern.startswith(case12):
                new_pattern = '{}{}'.format(pattern, case12)
                cls._appended_pattern = case12
            elif tail == 'tail_just_whitespace_plus' and not pattern.startswith(case13):
                new_pattern = '{}{}'.format(pattern, case13)
                cls._appended_pattern = case13
            elif tail == 'tail_just_whitespaces' and not pattern.startswith(case13):
                new_pattern = '{}{}'.format(pattern, case13)
                cls._appended_pattern = case13
            else:
                new_pattern = pattern
            return new_pattern
        return pattern

    @classmethod
    def add_repetition(cls, lst, repetition=''):
        """insert regex repetition for a first item of list

        Parameters
        ----------
        lst (lst): a list of sub pattens
        repetition (str): a repetition expression.  Default is empty.

        Returns
        -------
        list: a new list if repetition is required.
        """
        if not repetition:
            return lst

        new_lst = lst[:]
        item = new_lst[0]

        is_singular = ElementPattern.is_singular_pattern(item)
        item = item if is_singular else '({})'.format(item)

        _, m, *last = repetition.split('_', 2)
        if last:
            n = last[0]
            new_lst[0] = '%s{%s,%s}' % (item, m, n)
        else:
            new_lst[0] = '%s{%s}' % (item, m)
        return new_lst

    @classmethod
    def add_occurrence(cls, lst, occurrence=''):
        """insert regex occurrence for a first item of list

        Parameters
        ----------
        lst (lst): a list of sub pattens
        occurrence (str): an occurrence expression.  Default is empty.

        Returns
        -------
        list: a new list if occurrence is happened.
        """
        if not occurrence:
            return lst

        new_lst = lst[:]
        m = re.match(cls.occurrence_pattern, occurrence)
        is_phrase = bool(m.group('is_phrase'))

        fda, lda = m.group('fda') or '', m.group('lda') or ''
        fdb, ldb = m.group('fdb') or '', m.group('ldb') or ''
        fdc, ldc = m.group('fdc') or '', m.group('ldc') or ''
        fdd, ldd = m.group('fdd') or '', m.group('fdd') or ''

        func = ElementPattern.add_case_occurrence

        is_case_a = func(new_lst, fda, lda, is_phrase)
        is_case_b = is_case_a or func(new_lst, fdb, ldb, is_phrase)
        is_case_c = is_case_b or func(new_lst, fdc, ldc, is_phrase)
        is_case_c or func(new_lst, fdd, ldd, is_phrase)

        return new_lst

    @classmethod
    def add_case_occurrence(cls, lst, first, last, is_phrase):
        """check if pattern is a singular pattern

        Parameters
        ----------
        lst (str): a list.
        first (str): a first digit or option of case.
        last (str): a last digit or option of case.
        is_phrase (bool): a flag for matching a group of occurrences.

        Returns
        -------
        bool: True if occurrence happened, otherwise False.
        """
        if not first and not last:
            return False

        item = lst[0]
        if is_phrase:
            item = '{0}( {0})'.format(item)
        else:
            is_singular = ElementPattern.is_singular_pattern(item)
            item = item if is_singular else '({})'.format(item)

        first = int(first) if first.isdigit() else first
        last = int(last) if last.isdigit() else last

        if first == 'least' or first == 'most':
            if last == 0:
                fmt = '%s*' if first == 'least' else '%s?'
            else:
                fmt = '%%s{%s,}' if first == 'least' else '%%s{,%s}'
                fmt = fmt % last
        elif last == 'more':
            fmt = '%s*' if first == 0 else '%s+' if first == 1 else '%%s{%s,}' % first
        elif first == last:
            fmt = '%s' if first == 1 else '%%s{%s}' % first if first else '%s?'
        else:
            first, last = min(first, last), max(first, last)
            fmt = '%s?' if first == 0 and last == 1 else '%%s{%s,%s}' % (first, last)

        if fmt:
            lst[0] = fmt % item
            return True
        else:
            return False

    @classmethod
    def is_singular_pattern(cls, pattern):
        """check if pattern is a singular pattern

        Parameters
        ----------
        pattern (str): a pattern.

        Returns
        -------
        bool: True if pattern is a singular pattern, otherwise False.
        """
        left_bracket, right_bracket = '[', ']'
        pattern = str(pattern)
        first, last = pattern[:1], pattern[-1:]
        total = len(pattern)
        is_singular = total <= 1
        is_escape = total == 2 and first == '\\'
        is_char_set = pattern.count(first) == 1 and first == left_bracket
        is_char_set &= pattern.count(last) == 1 and last == right_bracket
        return is_singular or is_escape or is_char_set

    def remove_head_of_string(self):
        """remove a start of string pattern i.e ^ or ^\\s* or ^\\s+ or ^ * or ^ +

        Returns
        -------
        ElementPattern: new ElementPattern
        """
        if self.prepended_pattern and self.startswith('^'):
            pattern = str(self)[len(self.prepended_pattern):]
            new_instance = ElementPattern(pattern, as_is=True)
            new_instance.as_is = False
            new_instance.variable = copy(self.variable)
            new_instance.or_empty = self.or_empty
            new_instance.prepended_pattern = ''
            new_instance.appended_pattern = self.appended_pattern
        else:
            new_instance = copy(self)

        return new_instance

    def remove_tail_of_string(self):
        """remove an end of string pattern i.e $ or \\s*$ or \\s+$ or  *$ or  +$

        Returns
        -------
        ElementPattern: new ElementPattern
        """
        if self.appended_pattern and self.endswith('$'):
            pattern = str(self)[:-len(self.appended_pattern)]
            new_instance = ElementPattern(pattern, as_is=True)
            new_instance.as_is = False
            new_instance.variable = copy(self.variable)
            new_instance.or_empty = self.or_empty
            new_instance.prepended_pattern = self.prepended_pattern
            new_instance.appended_pattern = ''
        else:
            new_instance = copy(self)

        return new_instance


class LinePattern(str):
    """Use to convert a line text to regex pattern

    Attributes:
    variables (list): a list of pattern variable
    items (list): a list of sub-pattern

    Properties
    ----------
    statement (str): a template statement

    Parameters
    ----------
    text (str): a text.
    prepended_ws (bool): prepend a whitespace at the beginning of a pattern.
            Default is False.
    appended_ws (bool): append a whitespace at the end of a pattern.
            Default is False.
    ignore_case (bool): prepend (?i) at the beginning of a pattern.
            Default is False.

    Methods
    -------
    LinePattern.get_pattern(text) -> str
    LinePattern.readjust_if_or_empty(lst) -> None
    LinePattern.ensure_start_of_line_pattern(lst) -> None
    LinePattern.ensure_end_of_line_pattern(lst) -> None
    LinePattern.prepend_whitespace(lst) -> None
    LinePattern.prepend_ignorecase_flag(lst) -> None
    LinePattern.append_whitespace(lst) -> None

    Raises
    ------
    LinePatternError: raise an exception if pattern is invalid.

    """

    _variables = None

    def __new__(cls, text, prepended_ws=False, appended_ws=False,
                ignore_case=False):
        cls._variables = list()
        cls._items = list()
        data = str(text)
        if data:
            pattern = cls.get_pattern(
                data, prepended_ws=prepended_ws,
                appended_ws=appended_ws, ignore_case=ignore_case
            )
        else:
            pattern = r'^\s*$'
        return str.__new__(cls, pattern)

    def __init__(self, text,
                 prepended_ws=False, appended_ws=False,
                 ignore_case=False):
        self.text = text
        self.prepended_ws = prepended_ws
        self.appended_ws = appended_ws
        self.ignore_case = ignore_case

        self.variables = self._variables
        self.items = self._items

        # clear class variable after initialization
        self._variables = list()
        self._items = list()

    @property
    def statement(self):
        lst = []
        for item in self.items:
            if isinstance(item, ElementPattern):
                if not item.variable.is_empty:
                    lst.append(item.variable.var_name)
                else:
                    lst.append(item)
            else:
                lst.append(item)
        return ''.join(lst)

    @classmethod
    def get_pattern(cls, text,
                    prepended_ws=False, appended_ws=False,
                    ignore_case=False):
        """convert text to regex pattern

        Parameters
        ----------
        text (str): a text
        prepended_ws (bool): prepend a whitespace at the beginning of a pattern.
                Default is False.
        appended_ws (bool): append a whitespace at the end of a pattern.
                Default is False.
        ignore_case (bool): prepend (?i) at the beginning of a pattern.
                Default is False.

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        LinePatternError: raise an exception if pattern is invalid.
        """
        line = str(text)

        lst = []
        start = 0
        m = None
        for m in re.finditer(r'\w+[(][^)]*[)]', line):
            pre_match = m.string[start:m.start()]
            if pre_match:
                lst.append(TextPattern(pre_match))
            elm_pat = ElementPattern(m.group())
            if not elm_pat.variable.is_empty:
                cls._variables.append(elm_pat.variable)
            lst.append(elm_pat)
            start = m.end()
        else:
            if m and start:
                after_match = m.string[start:]
                if after_match:
                    lst.append(TextPattern(after_match))

        if len(lst) == 1 and lst[0].strip() == '':
            return r'^\s*$'
        elif not lst:
            if line.strip() == '':
                return r'^\s*$'
            lst.append(TextPattern(line))

        cls.readjust_if_or_empty(lst)
        cls.ensure_start_of_line_pattern(lst)
        cls.ensure_end_of_line_pattern(lst)
        prepended_ws and cls.prepend_whitespace(lst)
        ignore_case and cls.prepend_ignorecase_flag(lst)
        appended_ws and cls.append_whitespace(lst)
        cls._items = lst
        pattern = ''.join(lst)
        validate_pattern(pattern, exception_cls=LinePatternError)
        return pattern

    @classmethod
    def readjust_if_or_empty(cls, lst):
        """readjust pattern if ElementPattern has or_empty flag

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if len(lst) < 2:
            return

        total = len(lst)

        ws_pat = r'\s*'
        for index, item in enumerate(lst[1:], 1):
            prev_item = lst[index-1]
            is_prev_item_text_pat = isinstance(prev_item, (TextPattern, str))
            is_item_elm_pat = isinstance(item, ElementPattern)
            if is_prev_item_text_pat and is_item_elm_pat:
                if item.or_empty:
                    if prev_item.endswith(' '):
                        lst[index-1] = prev_item.rstrip() + ws_pat
                    elif prev_item.endswith(r'\s'):
                        lst[index-1] = prev_item + '*'
                    elif index == total - 1:
                        if prev_item.endswith(' +'):
                            lst[index-1] = prev_item[:-2] + ws_pat
                        elif prev_item.endswith(r'\s+'):
                            lst[index-1] = prev_item[:-3] + ws_pat

        index = len(lst) - 1
        is_stopped = False
        while index > 0 and not is_stopped:
            prev_item, item = lst[index-1], lst[index]
            is_prev_item_text_pat = isinstance(prev_item, (TextPattern, str))
            is_item_elm_pat = isinstance(item, ElementPattern)
            if is_prev_item_text_pat and is_item_elm_pat:
                if item.or_empty:
                    if prev_item.endswith(' '):
                        lst[index - 1] = prev_item.rstrip() + ws_pat
                    elif prev_item.endswith(r'\s'):
                        lst[index - 1] = prev_item + '*'
                    elif prev_item.endswith(' +'):
                        lst[index - 1] = prev_item[:-2] + ws_pat
                    elif prev_item.endswith(r'\s+'):
                        lst[index - 1] = prev_item[:-3] + ws_pat
            else:
                is_stopped = True
            index -= 2

        index = len(lst) - 1
        is_stopped = False
        is_prev_containing_empty = False
        while index > 0 and not is_stopped:
            prev_item, item = lst[index-1], lst[index]
            is_prev_item_elm_pat = isinstance(prev_item, ElementPattern)
            is_item_text_pat = isinstance(item, (TextPattern, str))
            if is_prev_item_elm_pat and is_item_text_pat:
                if prev_item.or_empty:
                    if item in [' ', ' +', r'\s', r'\s+']:
                        lst[index] = ws_pat
                    is_prev_containing_empty = True
                else:
                    if item in [' ', ' +', r'\s', r'\s+'] and is_prev_containing_empty:
                        lst[index] = ws_pat
                    is_prev_containing_empty = False
            else:
                is_stopped = True
            index -= 2

    @classmethod
    def ensure_start_of_line_pattern(cls, lst):
        """Ensure a start pattern does not contain duplicate whitespace

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if len(lst) < 2:
            return

        curr, nxt = lst[0], lst[1]

        if curr == '^':
            if isinstance(nxt, TextPattern):
                if nxt == ' ':
                    lst.pop(1)
                    return
                if re.match(' [^+*]', nxt):
                    lst[1] = nxt.lstrip()
                    return

        match = re.match(r'(?P<pre_ws>( |\\s)[*+]*)', nxt)
        if re.match(r'(\^|\\A)( |\\s)[*+]*$', curr):
            if isinstance(nxt, TextPattern) and match:
                index = len(match.group('pre_ws'))
                new_val = nxt[index:]
                if new_val == '':
                    lst.pop(1)
                else:
                    lst[1] = new_val

        # clean up any invalid a start of string pattern
        for index, node in enumerate(lst[1:], 1):
            if isinstance(node, ElementPattern) and node.prepended_pattern:
                lst[index] = node.remove_head_of_string()

    @classmethod
    def ensure_end_of_line_pattern(cls, lst):
        """Ensure an end pattern does not contain duplicate whitespace

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if len(lst) < 2:
            return

        last, prev = lst[-1], lst[-2]

        if last == '$':
            if isinstance(prev, TextPattern):
                if prev == ' ':
                    lst.pop(-2)
                    return
                if not re.search(' [+*]$', prev):
                    lst[-2] = prev.rstrip()
                    return

        match = re.search(r'(?P<post_ws>( |\\s)[*+]*)$', prev)
        if re.match(r'( |\\s)[*+]?(\$|\\Z)$', last):
            if isinstance(prev, TextPattern) and match:
                index = len(match.group('post_ws'))
                new_val = prev[:-index]
                if new_val == '':
                    lst.pop(-2)
                else:
                    lst[-2] = new_val

        # clean up any invalid a start of string pattern
        for index, node in enumerate(lst[:-1]):
            if isinstance(node, ElementPattern) and node.appended_pattern:
                lst[index] = node.remove_tail_of_string()

    @classmethod
    def prepend_whitespace(cls, lst):
        """prepend whitespace pattern to list

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if not lst:
            return

        pat = r'(\^|\\A)( |\\s)[*+]?'
        if not re.match(pat, lst[0]):
            lst.insert(0, r'^\s*')

    @classmethod
    def prepend_ignorecase_flag(cls, lst):
        """prepend regex ignorecase flag, i.e. (?i) to list

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if not lst:
            return

        pat = r'[(][?]i[)]'
        if not re.match(pat, lst[0]):
            lst.insert(0, '(?i)')

    @classmethod
    def append_whitespace(cls, lst):
        """append whitespace pattern to list

        Parameters
        ----------
        lst (list): a list of pattern
        """
        if not lst:
            return
        pat = r'( |\\s)[*+]?(\$|\\Z)$'
        if not re.search(pat, lst[-1]):
            lst.append(r'\s*$')


class MultilinePattern(str):
    """Use to convert multiple lines to regex pattern

    Parameters
    ----------
    text (str): a text.
    ignore_case (bool): prepend (?i) at the beginning of a pattern.
            Default is False.

    """
    def __new__(cls, text, ignore_case=False):

        lines = []
        if isinstance(text, (list, tuple)):
            for line in text:
                lines.extend(str(line).splitlines())
        elif isinstance(text, str):
            lines = text.splitlines()
        else:
            'text argument must be string or list of string'
            raise MultilinePatternError(text)

        if lines:
            pattern = cls.get_pattern(lines, ignore_case=ignore_case)
        else:
            pattern = r'^\s*$'
        return str.__new__(cls, pattern)

    @classmethod
    def get_pattern(cls, lines, ignore_case=False):
        """convert text to regex pattern

        Parameters
        ----------
        lines (lines): list of string
        ignore_case (bool): prepend (?i) at the beginning of a pattern.
                Default is False.

        Returns
        -------
        str: a regex pattern.

        """

        if not lines:
            return r'^\s*$'

        line_patterns = []
        for line in lines:
            line_pat = LinePattern(line, ignore_case=ignore_case)
            line_patterns.append(line_pat)

        first, last = line_patterns[0], line_patterns[-1]
        last = line_patterns[-1]

        if len(line_patterns) == 1:
            return first

        new_line_patterns = [cls.reformat(first, is_first=True)]
        other_line_pat = r'([^\r\n]*[\r\n]+)*'
        for line_pat in line_patterns[1:-1]:
            new_line_patterns.append(other_line_pat)
            new_line_patterns.append(cls.reformat(line_pat))

        new_line_patterns.append(other_line_pat)
        new_line_patterns.append(cls.reformat(last, is_last=True))

        new_pattern = ''.join(new_line_patterns)
        return new_pattern

    @classmethod
    def reformat(cls, pattern, is_first=False, is_last=False):
        """reformat pattern to work with re.MULTILINE matching

        Parameters
        ----------
        pattern (LinePattern, str): a line pattern.
        is_first (bool): indicator to tell that is a first line.  Default is False.
        is_last (bool): indicator to tell that is a last line.  Default is False.

        Returns
        -------
        str: a new pattern after reformat.
        """
        if is_first:
            if pattern.startswith('(?i)'):
                new_pattern = pattern.replace('(?i)', '(?im)')
            else:
                new_pattern = '(?m){}'.format(pattern)
        else:
            new_pattern = pattern.replace('(?i)', '')

        if not is_last:
            if new_pattern.endswith('$'):
                new_pattern = r'{}[\r\n]+'.format(new_pattern)
            else:
                new_pattern = r'{}[^\r\n]*[\r\n]+'.format(new_pattern)

        return new_pattern


class PatternBuilder(str):
    """Use to convert a list of text to regex pattern

    Parameters
    ----------
    lst_of_text (list): a list of text.
    var_name (str): a pattern variable.
    word_bound (str): word bound case.  Default is empty.
            value of word_bound can be word_bound, word_bound_left,
            or word_bound_right

    Methods
    -------
    PatternBuilder.get_pattern(text) -> str
    PatternBuilder.get_alnum_pattern(text) -> str
    PatternBuilder.add_var_name(pattern, name='') -> str

    Raises
    ------
    PatternBuilderError: raise an exception if pattern is invalid.
    """
    def __new__(cls, lst_of_text, var_name='', word_bound=''):
        if not isinstance(lst_of_text, (list, tuple)):
            lst_of_text = [lst_of_text]

        lst = []
        is_empty = False
        for text in lst_of_text:
            data = str(text)
            if data:
                pattern = cls.get_pattern(data)
                pattern not in lst and lst.append(pattern)
            else:
                is_empty = True

        is_empty and lst.append('')
        pattern = ElementPattern.join_list(lst)
        pattern = ElementPattern.add_word_bound(pattern, word_bound=word_bound)
        pattern = cls.add_var_name(pattern, name=var_name)
        validate_pattern(pattern, exception_cls=PatternBuilderError)
        return str.__new__(cls, pattern)

    @classmethod
    def get_pattern(cls, text):
        """convert text to regex pattern

        Parameters
        ----------
        text (str): a text

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        PatternBuilderError: raise an exception if pattern is invalid.
        """
        start = 0
        lst = []

        for m in re.finditer(r'[^a-zA-Z0-9]+', text):
            before_match = text[start:m.start()]
            lst.append(cls.get_alnum_pattern(before_match))
            lst.append(TextPattern(m.group()))
            start = m.end()
        else:
            if start > 0:
                after_match = text[start:]
                lst.append(cls.get_alnum_pattern(after_match))

        pattern = ''.join(lst) if lst else cls.get_alnum_pattern(text)
        validate_pattern(pattern, exception_cls=PatternBuilderError)
        return pattern

    @classmethod
    def get_alnum_pattern(cls, text):
        if text:
            if text.isdigit():
                return '[0-9]+'
            elif text.isalpha():
                return '[a-zA-Z]+'
            elif text.isalnum():
                return '[a-zA-Z0-9]+'
            else:
                return '.*'
        else:
            return ''

    @classmethod
    def add_var_name(cls, pattern, name=''):
        """add var name to regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        name (str): a regex variable name

        Returns
        -------
        str: new pattern with variable name.
        """
        if name:
            new_pattern = '(?P<{}>{})'.format(name, pattern)
            return new_pattern
        return pattern
