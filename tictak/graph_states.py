import main
import matplotlib.pyplot as plt

dic = main.main()

plt.plot(list(dic.keys()), list(dic.values()), 'go')
plt.show()
