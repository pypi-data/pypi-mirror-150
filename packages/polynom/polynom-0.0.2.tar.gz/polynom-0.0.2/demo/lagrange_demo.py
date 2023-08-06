from polynom import LagrangeBase

import matplotlib.pyplot as plt
import numpy as np


order_offset = 0  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)
# order_offset = 1  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)
# order_offset = 2  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)


lag_inst = LagrangeBase(coeff=[1.0, 2.0, 3.0, 4.0], t_ref=[-2.0, -1.0, 1.0, 2.0])


fig, ax = plt.subplots()

t = np.arange(-3.0, 3.0, 0.01)
s = lag_inst(t, cap_order_4_diff=order_offset)[order_offset, :]

t_refs = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
out = lag_inst(t_refs, cap_order_4_diff = order_offset + 1)
for i, t_refs_i in enumerate(t_refs):
    ax.plot(t, out[order_offset, i] + out[1 + order_offset, i]*(t - t_refs_i), 'k--')
ax.plot(t, s, 'b')
for i, t_refs_i in enumerate(t_refs):
    ax.plot(t_refs_i, out[order_offset, i], 'ro')

ax.set(xlabel='t', ylabel='p(t)',
       title='polynomial in Lagrange Base representation with a few selected tangents')
ax.grid()
bot, top = min(s), max(s)
diam = top - bot
plt.ylim(bot - 0.1*diam, top + 0.1*diam)

plt.show()
