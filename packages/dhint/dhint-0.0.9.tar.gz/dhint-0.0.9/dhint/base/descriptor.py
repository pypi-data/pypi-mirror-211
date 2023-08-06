from __future__ import annotations

__all__ = ['BaseDescriptor']

from abc import ABC
from typing import Callable, Optional, Any, ClassVar, Union
from dataclasses import MISSING


class BaseDescriptor(ABC):
    FIELD_TYPE: ClassVar[Optional[type]] = None
    HTML_TAG: ClassVar[Optional[str]] = None
    INPUT_TYPE: ClassVar[Optional[str]] = None
    FROZEN: ClassVar[Optional[bool]] = None
    DATALIST: ClassVar[Optional[bool]] = None
    HTMX: ClassVar[Optional[bool]] = None

    
    def __init__(self, *args, **kwargs):
        self.args: tuple[str] = tuple([str(item) for item in args if all([isinstance(item, str), (item != '')])])
        self._label: Optional[str] = kwargs.pop('label', None)
        self._hash: Optional[bool] = kwargs.pop('hash', None)
        self._compare: bool = kwargs.pop('compare', True)
        self._private: bool = kwargs.pop('private', False)
        self._repr: bool = kwargs.pop('repr', True)
        self._db: bool = kwargs.pop('db', True)
        self._form: bool = kwargs.pop('form', True)
        self._frozen: bool = kwargs.pop('frozen', False)
        self._html_tag: Optional[str] = kwargs.pop('html_tag', None)
        self._input_type: Optional[str] = kwargs.pop('input_type', None)
        self._search: Optional[bool] = kwargs.pop('search', False)
        self._datalist: Optional[bool] = kwargs.pop('datalist', False)
        self._htmx: Optional[str] = kwargs.pop('htmx', None)
        self._required: Optional[bool] = kwargs.pop('required', False)
        self._multiple: Optional[bool] = kwargs.pop('multiple', False)
        self._metadata: Optional[dict[str, Any]] = kwargs.pop('metadata', dict())
        self._default = kwargs.pop('default', MISSING if self.is_required else None)
        self._default_factory: Callable = kwargs.pop('default_factory', MISSING)
        self.extra_kwargs = kwargs
    
    def __repr__(self):
        return f'<class {type(self).__name__}: {self.fullname}>'
    
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_{name}'
        self.owner: 'BaseDetaModel' = owner
    
    def __set__(self, instance, value):
        setattr(instance, self.private_name, self.find_and_validate(instance, value))
    
    def __get__(self, instance, owner=None):
        if instance is None:
            return self.default
        return getattr(instance, self.private_name)
    
    @property
    def field_type(self):
        return self.FIELD_TYPE or self.owner.init_fields()[self.public_name].type
    
    def get_default(self):
        if self.default_factory is not MISSING:
            return self.default_factory()
        elif self.default is not MISSING:
            return self.default
        return None
    
    @property
    def default_factory(self) -> Union[Callable, MISSING]:
        return self._default_factory
    
    @property
    def default(self) -> Any:
        if self._default_factory is not MISSING:
            return None
        return self._default
    
    def frozen_value(self, instance, value):
        """If descriptor is frozen, try to recovery value already setted. If no value setted, passes the value unchanged."""
        return getattr(instance, self.private_name, value)
    
    def default_factory_if_none(self, value):
        """
        Apply the default_factory if value is None or empty string.
        If default_factory is MISSING or value exist, return the value unchanged.
        """
        if any([(value is None), (value == '')]):
            if self.default_factory is not MISSING:
                return self.default_factory()
        return value
    
    def process_value(self, instance, value):
        """Used inside __set__ to process the value recovering (if frozen) or applying a default_factory """
        if self.frozen:
            value = self.frozen_value(instance, value)
        return self.default_factory_if_none(value)
    
    def parse(self, value):
        """Try to parse the value for type expected if needed"""
        return value
    
    def validate(self, value) -> None:
        """Validate the value if needed"""
        pass
    
    def find_value(self, instance, value):
        """Process and parse the value"""
        return self.parse(self.process_value(instance, value))
    
    def find_and_validate(self, instance, value):
        """Process, parse and validate the value, returning the result value to be set at instance"""
        parsed = self.find_value(instance, value)
        self.validate(parsed)
        return parsed
    
    @property
    def owner_name(self):
        return self.owner.__name__
    
    def get(self, instance):
        return self.__get__(instance)
    
    @property
    def metadata(self):
        return self._metadata
    
    @property
    def htmx(self):
        return True if any([self._htmx is True, self.HTMX is True]) else False
    
    @property
    def datalist(self):
        return True if any([self._datalist is True, self.DATALIST is True]) else False
    
    @property
    def datalist_id(self):
        return f'{self.public_name}-list'
    
    @property
    def field_bs_class(self):
        if not self.no_form:
            if self.is_textarea:
                return 'form-control'
            elif self.is_select:
                return 'form-select'
            elif self.is_input:
                if self.is_range:
                    return 'form-range'
                elif self.is_checkbox:
                    return 'form-check-input'
                return 'form-control'
        return None
    
    @property
    def label_bs_class(self):
        if not self.no_form:
            if self.is_range:
                return 'form-check-label'
            elif self.is_hidden:
                return None
            return 'form-label'
        return None
    
    @property
    def label(self):
        return self._label or self.public_name
    
    @property
    def label_element(self):
        if not self.no_form:
            if not self.is_hidden:
                return '<label id="{}" for="{}">{}</label>'.format(
                        f'{self.public_name}__label',
                        f'{self.public_name}__field',
                        self.label
                )
        return ''
    
    @property
    def html_tag(self) -> Optional[str]:
        return self._html_tag or self.HTML_TAG
    
    @property
    def input_type(self) -> Optional[str]:
        return self._input_type or self.INPUT_TYPE
    
    @property
    def fullname(self) -> str:
        return f'{self.owner_name}.{self.public_name}'
    
    @property
    def hash(self) -> Optional[bool]:
        return self._hash
    
    @property
    def compare(self) -> bool:
        return self._compare
    
    @property
    def frozen(self):
        return True if any([self._frozen is True, self.FROZEN is True]) else False
    
    @property
    def private(self) -> bool:
        return self._private
    
    @property
    def repr(self) -> bool:
        return all([self._repr, (not self.private)])
    
    @property
    def db(self) -> bool:
        return self._db
    
    @property
    def no_form(self) -> bool:
        return not self._form
    
    @property
    def is_input(self):
        return True if any([self._html_tag == 'input', self.HTML_TAG == 'input']) else False
    
    @property
    def is_select(self):
        return True if any([self._html_tag == 'select', self.HTML_TAG == 'select']) else False
    
    @property
    def is_textarea(self):
        return True if any([self._html_tag == 'textarea', self.HTML_TAG == 'textarea']) else False
    
    @property
    def is_hidden(self):
        return all([self.is_input is True, self.input_type == 'hidden'])
    
    @property
    def is_range(self):
        return all([self.is_input is True, self.input_type == 'range'])
    
    @property
    def is_checkbox(self):
        return all([self.is_input is True, self.input_type == 'checkbox'])
    
    @property
    def is_required(self):
        return any(['required' in self.args, self._required is True])
    
    @property
    def is_multiple(self):
        return any(['multiple' in self.args, self._multiple is True])
    
    @property
    def search(self):
        return self._search
    
    def options(self, default=None):
        if hasattr(self.field_type, 'options'):
            return self.field_type.options(default)
        return ''
    
    def datalist_element(self):
        if self.datalist:
            return '<datalist id="{}">{}</datalist>'.format(
                    self.datalist_id,
                    self.options()
            )
        return ''
    

        



