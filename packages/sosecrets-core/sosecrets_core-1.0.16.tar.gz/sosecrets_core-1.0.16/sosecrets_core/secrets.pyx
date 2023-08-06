#cython: language_level=3
cdef class Secret:

    cdef object inner_secret
    cdef readonly int expose_count
    cdef public int max_expose_count

    def __init__(self,
                 object value = None,
                 *,
                 object func = None,
                 tuple func_args = (),
                 dict func_kwargs = {},
                 int max_expose_count = -1):

        if func is not None and value is not None:
            raise ValueError("`Secret` cannot be initialized with both `value` positional argument and `func` keyword")

        if func is not None:
            value = func(*func_args, **func_kwargs)

        self.inner_secret = value
        self.expose_count = 0
        self.max_expose_count = max_expose_count

    cpdef object expose_secret(self):

        if self.max_expose_count >= 0:
            if self.expose_count < self.max_expose_count:
                self.expose_count += 1
                return self.inner_secret
            else:
                raise AttributeError('`Secret` cannot be exposed more than {} times'.format(self.max_expose_count))
        else:
            self.expose_count += 1
            return self.inner_secret

    def apply(self,
              object func,
              *,
              tuple func_args=tuple(),
              dict func_kwargs=dict()):

        return Secret(func(self.inner_secret, *func_args, **func_kwargs), max_expose_count=self.max_expose_count)

    def __get__(self,
                object inst,
                type owner):

        if inst is None:
            raise ValueError('`Secret` as a descriptor is inaccessible through the class')
        return self

    def __set__(self,
                object inst,
                object value):
                
        raise TypeError('`Secret` as a class attribute is immutable')

    