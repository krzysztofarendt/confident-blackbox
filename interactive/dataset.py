import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

#%% Make dataset
x, y = make_moons(n_samples=2000, shuffle=True, noise=0.7)

#%% Plot dataset
plt.scatter(x[:, 0], x[:, 1], c=y, alpha=0.5, cmap="Accent")
plt.show()

#%% Split data into training, adjustment, and test sets
tst_size = 50
adj_size = 500

x_trn, x_tst, y_trn, y_tst = train_test_split(x, y, test_size=tst_size, shuffle=True)
x_trn, x_adj, y_trn, y_adj = train_test_split(x_trn, y_trn, test_size=adj_size, shuffle=True)

#%% Make model
model = GaussianNB()
model.fit(x_trn, y_trn)

#%% Define score function
y_prob = model.predict_proba(x_adj)

def score(x):
    return 1 - x

#%% Compute quantiles
alpha = 0.01
size = y_adj.size
q = (size + 1) * (1 - alpha) / size
q_hat = np.quantile(score(y_prob), q, axis=0)

print("Use these quantiles to form a prediction set:")
print(q_hat)

#%% Prediction sets
y_prob = model.predict_proba(x_tst)
pred_set = score(y_prob) <= q_hat
print(f"Prediction sets ({100 - alpha * 100:.1f}% confidence level):")
print(pred_set)

#%% Plot prediction sets
# TODO: Verify below lines
plt.scatter(x[:, 0], x[:, 1], c=y, alpha=0.5, cmap="Accent")
plt.scatter(x_tst[:, 0][pred_set[:, 0]], x_tst[:, 1][pred_set[:, 0]], marker="+", c=y_tst[pred_set[:, 0]])
plt.scatter(x_tst[:, 0][~pred_set[:, 0]], x_tst[:, 1][~pred_set[:, 0]], marker="o", c=y_tst[~pred_set[:, 0]])
plt.show();
