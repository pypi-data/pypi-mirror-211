# manly_randomization_test

B. F. J. Manly was a statistician who wrote several influential books and papers on multivariate statistical methods, biostatistics, and methods for randomization tests.

A randomization test is a type of non-parametric test that allows us to test hypotheses without requiring assumptions about the specific distribution of the data. It's also known as a permutation test or re-randomization test.

In the case of comparing means between two groups, a randomization test can be used in place of a traditional t-test when the assumptions of the t-test are not met (for example, if the data do not follow a normal distribution, or if the sample size is very small).

Here is an overview of how a randomization test between means is conducted:

    Calculate the observed difference between the two group means. 
        This will serve as your test statistic.
    Combine all the observations from both groups into a single group.
    Randomly divide this combined group into two new groups, making sure the group sizes match the original group sizes.
    Calculate the mean difference for these randomized groups.
    Repeat steps 3-4 thousands of times, each time recording the calculated mean difference.
    Count the number of times the absolute value of the randomized mean difference is greater than or equal to the absolute value of the observed mean difference. 
        This will give you the p-value, or the probability of observing a mean difference as extreme as, or more extreme than, the observed mean difference under the null hypothesis.

The null hypothesis for this test is that the group labels do not matter; in other words, there is no difference in means between the two groups. If the p-value is less than your predetermined significance level (often 0.05), you would reject the null hypothesis and conclude that there is a statistically significant difference in means between the two groups.


## Usage
```python
from manly_randomization_test import RandomizationTest

group1 = np.array([1, 2, 3, 4, 5])
group2 = np.array([2, 3, 4, 5, 6])

test = RandomizationTest(group1, group2)
p_value = test.test()

print('p-value:', p_value)

```
