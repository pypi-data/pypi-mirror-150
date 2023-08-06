from polynom import LegendreBase

import matplotlib.pyplot as plt
import numpy as np


a, b = -2.0, 5.0


# order_offset = 0  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)
order_offset = 1  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)
# order_offset = 2  # 0 <= order_offset <= 2 (since the polynomial is of order 3, i.e. of order '2' + 1)


leg_inst = LegendreBase(coeff=[2.0, 10.0, 5.0, 5.0, -3.7, 0.1])
leg_inst.domain = (a, b)


fig, ax = plt.subplots()

t = np.arange(a, b + 0.011, 0.01)
s = leg_inst(t, cap_order_4_diff=order_offset)[order_offset, :]

t_refs = [a, a + (b - a)/6.0, a + (b - a)/3.0, a + (b - a)/2.0, a + 2.0*(b - a)/3.0, a + 5.0*(b - a)/6.0, b]
out = leg_inst(t_refs, cap_order_4_diff = order_offset + 1)
for i, t_refs_i in enumerate(t_refs):
    ax.plot(t, out[order_offset, i] + out[1 + order_offset, i]*(t - t_refs_i), 'k--')
ax.plot(t, s, 'b')
for i, t_refs_i in enumerate(t_refs):
    ax.plot(t_refs_i, out[order_offset, i], 'ro')

ax.set(xlabel='t', ylabel='p(t)',
       title='polynomial in Legendre Base representation with a few selected tangents')
ax.grid()
bot, top = min(s), max(s)
diam = top - bot
plt.ylim(bot - 0.1*diam, top + 0.1*diam)

plt.show()
