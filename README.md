# Leakage Detection Framework
This is a framework for TVLA. The goal of this framework is to make it easier for researchers, scientists, or anyone interested in using TVLA for leakage detection.

## Basics
We will demonstrate a few of the functionalities of the framework below.
<br>
The combinations of the features, best practice suggestions, and other advanced parts (e.g. plotting) will be discussed later on in the documentation. The details about the underlying implementation and ways of extension will be discussed in each individual component of the framework.
<br>
<br>
### The Main Framework Class
For basic functionality, the only class that needs to be imported is the *LeakageDetectionFramework*:


```python
from core import LeakageDetectionFramework
```

Using an instance of the *LeakageDetectionFramework*, we can already do a few basic things. We can already load trace data from an *npz* file that will automatically be loaded into and interpreted by a data handler class. We will touch on this later. For now we will focus on the framework instance itself, because the rest is happening under the hood.
The following code will load the trace data from the *npz* file and using Welch's t-test, it will calculate the t statistic.


```python
# Create the instance
ldf = LeakageDetectionFramework()

# Load the data
ldf.load_data("../traces/REASSURE_power_Unprotected_AES_fixed_vs_random_Exp1.npz")

# Calculate t_statistic using Welch's t-test
t_statistic = ldf.calculate_t_statistic()

# Get the indices of the leaky samples for further analysis
ind_from = 0
ind_to = 13900
range_of_measurement = range(ind_from, ind_to)
threshold = 4.5
leakage = ldf.indices_of_leaky_samples(t_statistic, range_of_measurement, threshold)
```

<br>
The above method is in case we would like to process the result ourselves. We could pring print, for example the number of total leaky points:


```python
leaky_indices = leakage==True
print('Number of leaky points: %.0f' % leakage[leaky_indices].sum())
```

    Number of leaky points: 9390


<br>
Or we could simply use the following function to achieve the same thing:


```python
ldf.number_of_leaky_points(t_statistic, range_of_measurement, threshold)
```




    9390



<br>
We could also look at all of the leaky points:


```python
reduced_t_stat = t_statistic[range_of_measurement]
print('Leaky points: \n%s' % reduced_t_stat[leaky_indices])
```

    Leaky points: 
    [ 17.21989285  18.9699006   18.14778368 ... -11.58778067 -12.74171359
     -13.55217319]


<br>
Or achieve the same result by using one of the functions of the framework:


```python
print(ldf.calculate_leaky_points(t_statistic, range_of_measurement, threshold))
```

    [ 17.21989285  18.9699006   18.14778368 ... -11.58778067 -12.74171359
     -13.55217319]


<br><br>
### Trace Data Class
The framework uses a few helper classes to keep everything more organized, maintainable and more easy to scale. One of these classes is called *TVLAData*. This is used to store the data that the framework loads from the *npz* file. We can use the functions of this helper class to fetch different parts of the information that we wish to work with, visualise, extend, etc.
<br>
The *TVLAData* class is designed to be a [singleton](https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm). The reason behind this decision is that we do not wish to create new instances every time we load data sets for our tests. This helps in keeping the data from different tests separated from each other, reducing the chances of mixing them up with one another.
<br>
Using the class is simple, but first we need to import it from the proper package:


```python
from data import TVLAData
```

<br>
After importing the class we can fetch the instance and use it.
<br>


```python
t_test_data = TVLAData.get_instance()
```

<b>Important note:</b> before using it we need to remember that in [this section](#The-Main-Framework-Class) we loaded the data from the *npz* file using the framework. This step is a must before fetching data from the class's instance.

<br>
#### Fetching Data From the File

To get all the trace data from the file:


```python
print('Every trace: \n%s' % t_test_data.get_all_traces())
```

    Every trace: 
    [482. 594. 416. ... 527. 626. 584.]


<br>
To get all the fixed traces from the file (this is based on the fixed flag that is used in the dataset):


```python
print('Fixed traces: \n%s' % t_test_data.get_every_fixed_trace())
```

    Fixed traces: 
    [[482. 594. 416. ... 527. 626. 584.]
     [502. 272. 410. ... 529. 633. 590.]
     [477. 588. 409. ... 514. 621. 580.]
     ...
     [493. 265. 405. ... 508. 616. 575.]
     [591. 271. 410. ... 528. 632. 589.]
     [592. 281. 412. ... 517. 624. 583.]]


<br>
To get all the random traces from the file (this is based on the fixed flag that is used in the dataset):


```python
print('Random traces: \n%s' % t_test_data.get_every_random_trace())
```

    Random traces: 
    [[593. 271. 410. ... 327. 466. 482.]
     [477. 587. 416. ... 511. 622. 586.]
     [595. 271. 405. ... 329. 466. 482.]
     ...
     [485. 595. 419. ... 155. 330. 379.]
     [494. 280. 416. ... 518. 623. 587.]
     [474. 586. 414. ... 320. 460. 478.]]


<br>
Currently, we have mostly seen the format that we imported from the *npz* file and used almost everything as arrays. It is sometimes useful to have the data in other formats too. For example, when we are using the plotting functionality of the framework, we need to use [*DataFrame*](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) class to visualize the data. This is part of the *pandas* library and it uses a tabular data format.

<br>
When we use the *DataFrame* class we can name the headers of the columns that will represent the data in the rows of our structure. For this we can use the following utility function of the *TVLAData* class:


```python
t_test_data.convert_t_statistic_to_data_frame(t_statistic)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Time Samples</th>
      <th>T-Statistic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>-0.229905</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.497942</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>0.651976</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>0.141892</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>0.010075</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15995</th>
      <td>15995</td>
      <td>31.082505</td>
    </tr>
    <tr>
      <th>15996</th>
      <td>15996</td>
      <td>31.730605</td>
    </tr>
    <tr>
      <th>15997</th>
      <td>15997</td>
      <td>33.544178</td>
    </tr>
    <tr>
      <th>15998</th>
      <td>15998</td>
      <td>32.846872</td>
    </tr>
    <tr>
      <th>15999</th>
      <td>15999</td>
      <td>32.032265</td>
    </tr>
  </tbody>
</table>
<p>16000 rows × 2 columns</p>
</div>



As we can see, by default the function names the headers of the two columns "Time Samples" and "T-Statistic". This is the default behaviour because this conversion is specifically useful when we would like to plot the T-Statistic data. The reason is that if we would like to use a pline plot and show the correct names of the x and y coordinates, then the *DataFrame* in this format is useful for this.
<br>
When we call the function above, under the hood we are actually using another function that is more generic and can be used for data other than T-Statistic. For example, if we would like to use the first set of the random traces and the time samples of those traces:


```python
time_samples = range(0, len(t_test_data.get_every_random_trace()[0]))
t_test_data.convert_to_data_frame(data_x=time_samples, data_y=t_test_data.get_every_random_trace()[0], x="t Samples", y="Random Traces")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>t Samples</th>
      <th>Random Traces</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>593.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>271.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>410.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>418.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>545.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15995</th>
      <td>15995</td>
      <td>589.0</td>
    </tr>
    <tr>
      <th>15996</th>
      <td>15996</td>
      <td>676.0</td>
    </tr>
    <tr>
      <th>15997</th>
      <td>15997</td>
      <td>327.0</td>
    </tr>
    <tr>
      <th>15998</th>
      <td>15998</td>
      <td>466.0</td>
    </tr>
    <tr>
      <th>15999</th>
      <td>15999</td>
      <td>482.0</td>
    </tr>
  </tbody>
</table>
<p>16000 rows × 2 columns</p>
</div>



Notice how the headers are not the same as in the example before because here we specified the values. This part is going to be especially useful when it comes to plotting.

<br><br>
### Plotting
In this section we discuss the plotting functionality of the framework.
Plotting any data can be achieved by fetching the plotter from the main instance of the framework class. We discussed about the main class above, where we instantiated it with the following code segment:


```python
ldf = LeakageDetectionFramework()
```

Using the main framework class, we can fetch an instance of the *Plotter* class. This class uses visualisation tools, such as [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) under the hood.
Getting a new instance of the *Plotter* class is simple:


```python
plotter = ldf.plotter()
```

#### Creating Plots
When it comes to working with plots, the most important aspect of this framework is ease of use. Plotting data in a fashion that it is simple and fast is not always possible. Many times we have to write many lines of code to properly configure a plot for a certain context (by context we mean plot type, size, etc.), not being able to simply create multiple plots reusing the same context. Moreover, if we want to create two plots of the same data in the same context, but just make the second plot a little bit different, for example by highlighting a few points, drawing a line to split the plot with a certain logic in mind, we cannot do it without having to rewrite the same 10-15 lines of code and adding the 2-3 lines that we need for the extra highlighting.

<br>
This is where this framework's *Plotter* class comes in. The direction we wanted to take this class was to make it as easy as possible for the users to create as many plots as they want without any of the headache certain libraries could give them.
The idea was to declare a **chain** of plots that the user would like to display and plot that without any additional parameter tweaking or other complicated things.

<br>
##### Example
Let's say that the user would like to compare two sets of data. In our case it would make sens to look at the initial power trace that we extract from the data file and the T-Statistic after our calculations. We already calculated everything above, so as we discussed in [this section](#Trace-Data-Class), we can just conveniently re-use the *TVLAData* class' instance and use the data for plotting.


```python
plotter.create_line_plot(t_statistic).plot()
```


    
![svg](main-app_files/main-app_35_0.svg)
    


Remember that we need to convert our data into *DataFrame* using the helper functions that we've discussed about above. Conveniently enough, the *Plotter* class takes care of this part for us. This way we are not forced to convert from our structure to *DataFrames* back and forth, we can just pass our data to the plotter and it will do the conversion locally so it can do the plotting without issues.

<br>
Note that we need to call the *plot* function at the end of the **chain** of functions when we are using the plotter.
We say chain because, let's say we would like to plot the T-Statistic and the original power trace next to each other. To achieve that we would need to call the function that we just used above twice:


```python
plotter.create_line_plot(t_statistic).create_line_plot(t_test_data.get_all_traces()).plot()
```


    
![svg](main-app_files/main-app_38_0.svg)
    



    
![svg](main-app_files/main-app_38_1.svg)
    


As we can see it is really simple to create two consecutive plots with different data. We can also observe that the default label for the x and y coordinates are "Length" and "Data". Fortunately, we can use arbitrary labels for the coordinates, we just have to pass them as parameters to the plotting functions as such:


```python
plotter.create_line_plot(t_statistic, x="Time Samples", y="T-Stat").create_line_plot(t_test_data.get_all_traces(), x="Time Samples", y="Traces").plot()
```


    
![svg](main-app_files/main-app_40_0.svg)
    



    
![svg](main-app_files/main-app_40_1.svg)
    


#### Using Decorators
To make our life easier when we work with such a framework, we could use decorators to ommit as many overhead as possible and get to the fun part, in this case the fun part is creating those beautiful plots and analyzing them. Luckily the framework contains a module with useful decorators that can help us.
<br>
Consider the scenario in which we are writing functions to plot our data. It would be much easier to ommit the 
