from string import ascii_uppercase
f = lambda x: (
  all([
    isinstance(x, str),
    not (' ' in x and x[:3] != 'El '),
    x[0] in ascii_uppercase]) if len(x)
  else False
)
t = lambda: all([
  f('Forbes'),
  f('El Sawah'),
  not any([f(_) for _ in ['New York', 'apple', '']])
])
