import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import math
import scipy.stats as stats

def make_pretty(ax, title='', xTitle='', yTitle=''):
    '''
    Purpose: This function makes a few basic cosmetic adjustments to an input axes object.
             The objective is to serve as a "quick and dirty" way to make a plot more presentable.

    Input:
        - ax     (matplotlib axes object) : The axes object to which cosmetic adjustments will be made
        - title  (str)                    : Desired plot title
        - xTitle (str)                    : Desired x-axis label
        - yTitle (str)                    : Desired y-axis label

    Output: 
        - There is no output. The orginal copy of ax is altered directly.

    '''
    ax.spines['left'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['right'].set_color('black')

    ax.spines['left'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel(xTitle, fontsize=16)
    ax.yaxis.set_label_coords(-0.15, 0.5)
    ax.set_ylabel(yTitle, rotation = 'horizontal', fontsize = 16)
    
    ax.tick_params(axis='both', labelsize = 16)
    
    ax.grid(True)
    return


def scatter_bygroup(ax, x,y,col,colmap='hot'):
    '''
    Purpose:
        - Plot y against x in a scatterplot, where the points are coloured by a third variable, col.

    Input:
        - ax  (matplotlib axis) : The axis on which to add the scatter plot
        - x   (array/float)     : The data for the x-axis of the scatterplot
        - y   (array/float)     : The data for the y-axis of the scatterplot
        - col (list)            : A list of values of some variable which will correspond to groups. This 
                                  value is used to determine the colour of a point. Points with the same 
                                  'col' value will have the same colour.
        - colmap (str)          : A colormap for determining the group colours. Default to 'hot'.

   Output:
	- Note that there is no output, however, the original input axes object will be altered.
 
    '''
    # Set the color map to match the number of species
    uniq = list(set(col))
    z    = range(1,len(uniq))
   
    cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colmap)

    
    # Plot each group
    for i in range(len(uniq)):
        indx = (col == uniq[i])
        ax.scatter(x[indx], y[indx], s=150, color=scalarMap.to_rgba(i), label=uniq[i])
    return



def moving_average_baseline_subtraction(current, window_size, forward = True):
    '''
    Purpose:
        An iterative function that estimates the baseline of an input signal using a peak-stripping 
        moving average (i.e. a moving average algorithm designed to strip baselines off of peaks.) 
        The function is intended to be used on voltammograms collected via sweep-like voltammetry.

        A simple plot is printed with the baseline estimate overlayed on the input signal.



    Input:
        - current (array/float) : An array of values intended to be a peak-like signal with baseline
        - window_size (int)     : An integer indicating the number of points to be contained in a single window
                                of the moving average
        - forward (boolean)     : This variable is relevant in the context of voltammetric sweep-like data collection.
                                If true, the data in "current" was collected via a sweep-like voltammetric scan where
                                the potential/voltage was swept from a starting value to an increasingly positive
                                potential. If False, the potential/voltage swept from a starting value to increasingly
                                negative values.
                                The objective is essentially to ensure that peak-like structures in the data are "above"
                                the baseline - i.e. more positive than the baseline. If the peaks manifests below the 
                                baseline in your data (i.e. "trench-like" as opposed to peak-like), set this variable to 
                                False, and the algorithm will adjust itself accordingly.
      

  
    Output:
        - baseline (array/float)           : An array of values containing the BASELINE estimate of the algorithm
        - baseline_fig (matplotlib figure) : An overlay plot of the orignal signal and the estimated baseline. Note that
                                             the plot is printed within the function in addition to this output.
    '''
    num_leftover = -1
    
    
    num_samples = len(current)
    num_averages = math.floor(len(current)/window_size)
    
    flag = False # True if the number of samples is a non-integral multiple of window size
    if num_averages*window_size < num_samples:
        flag = True
    
    
    averages = np.zeros(num_averages)
    for i in range(0, num_averages):
        count = i+1
        averages[i] = np.mean((current[(count-1)*window_size:(count*window_size-1)]))
    
    
    # I'm not sure how this is handled in the real Nova algorithm so for now I'm just flagging it.
    if flag:
        num_leftover = len(current) - num_averages*window_size
        
    # If data was obtained on a reverse sweep, we want to read it from right to left for the moving average. We achieve this by flipping the 
    # direction of 'current' below:
    if not forward:
        current = current.iloc[::-1]
   
    temp_averages = averages
    for iteration in range(1000):
        tally = 0
        if forward:
            for i in range(1, num_averages-1):
                # Think about what would happen to an apex in the following: 
                if np.mean((averages[i-1], averages[i+1])) < averages[i]:
                    temp_averages[i] = np.mean((averages[i-1], averages[i+1]))
                    tally += 1
        else:
            for i in range(1, num_averages-1):
                if averages[i] < np.mean((averages[i-1], averages[i+1])):
                    temp_averages[i] = np.mean((averages[i-1], averages[i+1]))
                    tally += 1
            
        
        averages = temp_averages
        if tally == 0:  
            break
        
    # Flip current back, if it is reverse sweep data, since we are done with the moving average portion:
    if not forward:
        current = current.iloc[::-1] 
        
        
    # Interpolate the "betweens":
    baseline = np.zeros(len(current))
    baseline[0] = current[0]
    for i in range(num_averages):
        count = i+1
        baseline[(count*window_size-1)] = averages[i] 
        slope = (averages[i] - averages[i-1])/window_size
        intercept = averages[i-1]
        if i == 0:
            intercept = baseline[0]
            slope = (averages[i] - intercept)/window_size

        start = count*window_size - window_size
        for j in range(1, window_size):            
            baseline[start+j-1] = intercept + slope*j
       
    if flag:
        num_samples = len(current)
        
        start = window_size*num_averages + 1
        
        for i in range(start, num_samples):
            baseline[i] = current[i]
            
            


    
      
        

    return baseline





def get_groupwise_intervals(xdom, yran):
    '''
    Purpose:
        The purpose of this function is to group the input data and then calculate the the means, confidence bands, and prediction bands 
        of each groups. A group is defined by a fixed value of xdom. If many points have the same value of xdom, then they form a group.
        
        The function will output a the interpolated means, confidence interval edges, prediction interval edges, and standard deviations
        of each group. 
        
    Input:
        - xdom (array/float) : an array of points defining the x-coordinates of observations
        - yran (array/float) : an array of points defininf the y-coordinates of observations
        
    Output:
        - outList (list) : list containing 7 arrays
                                1. xUnique    (array/float) : contains the unique xdom values that define the groupings
                                2. means      (array/float) : contains the mean of each group
                                3. sampleSigs (array/float) : the SAMPLE standard deviation of each group (n-1 denominator)
                                4. CILow      (array/float) : lower limits of the CI for the mean of each group
                                5. CIUpp      (array/float) : upper limits of the CI for the mean of each group
                                6. PILow      (array/float) : lower limits of the PI for new observations from each group
                                7. PIUpp      (array/float) : upper limits of the PI for new observations from each group
                                
                        Note that the ith entry in each of the 7 arrays are associated with each other. That is, the ith entry in each array
                        defines a property of the ith group.
                        
                        Note that the limits are calculated at the 95% confidence level and assuming normality of data (i.e. the typical 
                        Student's t multiple of the [group] sample standard deviation. The results may therefore be erroenous for non-normally
                        distributed data.    
    '''

    xUnique = np.unique(xdom) # creates an array of the unique values in xdom
    numGroups = len(xUnique)

    # Create arrays of zeros that will be populated with 
    # the corresponding stats about each group. There is 
    # one entry for each group - i.e. for each unique value
    # of xdom
    means      = np.zeros(numGroups)
    CILow      = np.zeros(numGroups)
    CIUpp      = np.zeros(numGroups)
    PILow      = np.zeros(numGroups)
    PIUpp      = np.zeros(numGroups)
    sampleSigs = np.zeros(numGroups)
    for groupIndex in range(numGroups):
        mask = [val == xUnique[groupIndex] for val in xdom]
        xdat = xdom[mask]
        ydat = yran[mask]


        means[groupIndex] = np.mean(ydat)

        delta = ydat - means[groupIndex]
        sampleSigs[groupIndex] = np.sqrt(np.dot(delta, delta)/(len(delta)-1))

        t = stats.t.ppf(0.975, len(delta)-1)


        CILow[groupIndex] = means[groupIndex] - t*sampleSigs[groupIndex]/np.sqrt(len(delta))
        CIUpp[groupIndex] = means[groupIndex] + t*sampleSigs[groupIndex]/np.sqrt(len(delta))

        PILow[groupIndex] = means[groupIndex] - t*sampleSigs[groupIndex]*np.sqrt(1+1/len(delta))
        PIUpp[groupIndex] = means[groupIndex] + t*sampleSigs[groupIndex]*np.sqrt(1+1/len(delta))
    
    outList = [xUnique, means, sampleSigs, CILow, CIUpp, PILow, PIUpp]
    return outList