'''
@filename: spectroscopy.py
@author: Md. Ziaul Hoque
@email: ziaul55@gmail.com
@created: 02.10.2018

@description: 
    A very simple graphical user interface to plot spectroscopy.
    
    In electron spectroscopy matter is examined by radiating it 
    with a bright light and measuring the kinetic energy of electrons 
    that come off it. When the photonic energy of light and kinetic 
    energy of the electrons are known, they can be used to derive the 
    amount of force that was required to break off the electrons. This 
    provides valuable information about the matter's electron structure, 
    and its chemical and physical properties. This phenomenon where 
    photons break off electrons is called photoionization, and the 
    broken off electrons are called photoelectrons.
    
    This project requires two third party libraries: numpy and matplotlib. 
    There are multiple ways to install them. Windows installers 
    can be found for both, and can also be installed them using pip. There 
    are also various full stack installers available in the internet (full 
    stack means they install Python along with a bunch of libraries, usually 
    replacing "generic" Python installation). 
    :numpy::
    :matplotlib::
'''

from matplotlib.widgets import TextBox
from os import walk
from tkinter import *
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np
import os, statistics


class Spectroscopy():
    """
    Initializing spectroscopy ...
    Please wait ...
    """
    print(__name__, __doc__)
    
    #class valribles
    widthpixels, heightpixels, selected_data_index, count_index = 340, 165, 0, 0
    title, required_extension, intensity_info = "Spectrocopy", '.txt', ['', '']
    data, binding_energies, intensities, selected_data_indices = [], [], [], []
    fig, ax, text_box, selected, line, pick_event, key_press_event = None, None, None, [None, None, None, None], None, None, None
    
    def __init__(self, gui):
        '''
        Congratulations! 
        Spectroscopy initialized successfully!! ...
        '''
        
        self.set_window_title(gui)
        self.set_non_resizable_window(gui)
        self.set_instructions(gui)
        self.set_buttons(gui)
        self.set_window_at_center(gui)
        
        
        print(self.__init__.__name__, self.__init__.__doc__)
        
    def set_window_at_center(self, gui):        
        '''
        Placing the window into the center of the screen ...
        '''
        print(self.set_window_at_center.__name__, self.set_window_at_center.__doc__)
        
        gui.update_idletasks()
        w = gui.winfo_screenwidth()
        h = gui.winfo_screenheight()
        size = tuple(int(_) for _ in gui.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        gui.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    def set_window_title(self, gui):
        '''
        Setting the window title ...
        '''
        print(self.set_window_title.__name__, self.set_window_title.__doc__)
        gui.title(self.title)
        
    def set_non_resizable_window(self, gui):
        '''
        Setting the window to non resizable ...
        '''
        print(self.set_non_resizable_window.__name__, self.set_non_resizable_window.__doc__)
        
        gui.geometry('{}x{}'.format(self.widthpixels, self.heightpixels))
        gui.resizable(width=False, height=False)
        
    def set_instructions(self, gui):
        '''
        Placing instructions ... 
        '''
        print(self.set_instructions.__name__, self.set_instructions.__doc__)
        
        # set instructions for user
        Label(gui, text="Instructions:").grid(row=0, columnspan = 2, sticky=W, padx=5, pady=5)
        Label(gui, text="(1) Click 'Load Data' button and specify spectrum data folder.").grid(row=1, columnspan = 2, sticky=W, padx=5, pady=5)
        Label(gui, text="(2) Click 'Plot Data' button to plot spectral data in a window.").grid(row=2, columnspan = 2, sticky=W, padx=5, pady=5)
        Label(gui, text="(3) Finally choose 2 sets of x (binding energies) values.").grid(row=3, columnspan = 2, sticky=W, padx=5, pady=5)
        
    def set_buttons(self, gui):
        '''
        Placing Load Data & Plot Data Buttons ...
        '''
        print(self.set_buttons.__name__, self.set_buttons.__doc__)
        
        Button(gui, text="Load Data", command=lambda:self.load_data()).grid(row=4, column=0, sticky=W, padx=5, pady=5)
        Button(gui, text="Plot Data", command=self.plot_data).grid(row=4, column=1, sticky=E, padx=5, pady=5)
    
    def load_data(self):
        '''
        loading directory chooser ...
        '''
        print(self.load_data.__name__, self.load_data.__doc__)
        
        directory = filedialog.askdirectory(title = "Select Directory")
        if directory: 
            try: 
                self.data = self.read_data(directory)
            except Exception as error: 
                print(error)
                messagebox.showerror("Failed!", "Failed to read '%s'"%directory)
        else:
            messagebox.showerror("Failed!", "Please choose a directory!!")
    
    def read_data(self, chosen_directory):
        '''
        Reading directory files ...
        '''
        print(self.read_data.__name__, self.read_data.__doc__)
        
        # list of files that are in the 'chosen_directory'
        files = []
        for (dirpath, dirnames, filenames) in walk(chosen_directory):
            files.extend(filenames)
            break
        # readable files those are with 'required_file_extension'
        required_file_extension = self.required_extension
        tuples = []
        for filename in files:
            file_name, file_extension = os.path.splitext(filename)
            if required_file_extension == file_extension:        
                is_corrupted = False
                temporary_tuples = []
                try:
                    # replace \ [backward slash] by / [forward slash]
                    #file_name_2 = r"{}".format(chosen_directory + '\\' + filename).replace("\\", '/')
                    file_name_2 = r"{}".format(chosen_directory + '/' + filename)
                    file = open(file_name_2, 'r')
                    lines = file.read().strip("\n").split("\n")
                    #index = 0
                    for line in lines: 
                        try:
                            # check whether the binding_energy is in the range of x-min & x-max
                            # if not in range then do not include into the list
                            binding_energy, intensity = line.split(' ')
                            binding_energy, intensity = float(binding_energy), float(intensity)
                            tuple = (float(binding_energy), float(intensity))
                            temporary_tuples.append(tuple)
                        except(ValueError):
                            is_corrupted = True
                            print("Broken file: ", filename)                        
                            break
                    file.close()
                except(FileNotFoundError):
                    pass
                if not is_corrupted:
                    for temporary_tuple in temporary_tuples:
                        tuples.append(temporary_tuple)
        return tuples
    
    def plot_data(self):
        '''
        Ploting data ...
        '''
        print(self.plot_data.__name__, self.plot_data.__doc__)
        
        if len(self.data) == 0:
            messagebox.showerror("Failed!", "No data loaded!!")
        else:
            # print([x for (x, y) in self.data])
            sorted(self.data)
            
            # remove background noises
            self.remove_noise()
            
            # spectrum in the given range
            self.binding_energies, self.intensities = self.spectrum_in_range()
            
            # window title    
            self.fig = plt.figure('Binding energy (eV) VS Intensity (arbitrary units)')
            self.ax = self.fig.add_subplot(111)
            plt.subplots_adjust(bottom=0.20) # postion of text box -- how far from original graph
            
            # figure title
            self.ax.set_title('Binding energy (eV) VS Intensity (arbitrary units)')
            self.ax.set_xlabel('Binding energy (eV)')
            self.ax.set_ylabel('Intensity (arbitrary units)')
            self.line, = self.ax.plot(self.binding_energies, self.intensities, '-', picker=5)  # 5 points tolerance
            
            self.text_box = self.set_text_box()
            self.selected[0], = self.ax.plot([self.binding_energies[0]], [self.intensities[0]], 'o', ms=12, alpha=0.4, color='#123abc', visible=False)
            self.selected[1], = self.ax.plot([self.binding_energies[0]], [self.intensities[0]], 'o', ms=12, alpha=0.4, color='#123abc', visible=False)
            self.selected[2], = self.ax.plot([self.binding_energies[0]], [self.intensities[0]], 'o', ms=12, alpha=0.4, color='#abc456', visible=False)
            self.selected[3], = self.ax.plot([self.binding_energies[0]], [self.intensities[0]], 'o', ms=12, alpha=0.4, color='#abc456', visible=False)
            
            self.pick_event = self.fig.canvas.mpl_connect('pick_event', self.onpick)
            self.key_press_event = self.fig.canvas.mpl_connect('key_press_event', self.onpress)
            
            plt.show()
        
    def find_slope(self, x1, y1, x2, y2):
        try:
            return (y2 - y1) / (x2 - x1)
        except(ValueError, ZeroDivisionError):
            return None
            
    def remove_noise(self):
        '''
        Removing noises ...
        '''
        
        first_binding_energy, last_binding_energy = self.data[0][0], self.data[-1][0]
        first_intensity, last_intensity = self.data[0][1], self.data[-1][1]
        slope = self.find_slope(first_binding_energy, first_intensity, last_binding_energy, last_intensity)
        
        '''
        y = m(x - x0) + y0
        here, m is slope
        '''
        for index in range(len(self.data)):
            (binding_energy_on_line, intensity_with_noise) = self.data[index]
            intensity_on_line = slope * (binding_energy_on_line - first_binding_energy) + first_intensity
            self.data[index] = (binding_energy_on_line, intensity_with_noise - intensity_on_line)
            
    def spectrum_in_range(self):
            
        binding_energies = [b for (b, i) in self.data[0:500]]
        intensities = [0 for x in range(0, 500)] # intializing 0's
        
        for x in range(0, len(self.data)):
            intensities[x % 500] += self.data[x][1]
            
        # check in range
        r_binding_energies = []
        r_intensities = []
        for x in range(0, len(binding_energies)):
            r_binding_energies.append(binding_energies[x])
            r_intensities.append(intensities[x])
        return r_binding_energies, r_intensities
        
    def set_text_box(self):
        axbox = plt.axes([0.125, 0.01, 0.775, 0.075])
        text_box = TextBox(axbox, '', initial='')
        return text_box
        
    def calculate_area(self, x_coordinates, y_coordinates):
        return np.trapz(y_coordinates, x=x_coordinates)
   
    def onpress(self, event):
    
        if self.selected_data_index is None:
            return
        if event.key not in ('n', 'p'):
            return
        if event.key == 'n':
            inc = 1
        else:
            inc = -1

        self.selected_data_index += inc
        self.selected_data_index = np.clip(self.selected_data_index, 0, len(self.binding_energies) - 1)
        self.update()

    def onpick(self, event):
        
        if event.artist != self.line:
            return True

        N = len(event.ind)
        if not N:
            return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata
        
        middle_index = statistics.median_high(event.ind)        
        #distances = min([np.hypot(x - self.binding_energies[index], y - self.intensities[index]) for index in event.ind])
        #indmin = distances.argmin()
        #data_index = event.ind[indmin]

        self.selected_data_index = middle_index
        self.update()

    def update(self):
    
        if self.selected_data_index is None:
            return
        
        data_index = self.selected_data_index
        self.selected_data_indices.append(data_index)
        
        self.selected[self.count_index].set_visible(True)
        self.selected[self.count_index].set_data(self.binding_energies[data_index], self.intensities[data_index])
        
        self.count_index += 1
        self.fig.canvas.draw()
        
        if self.count_index == 4:
            start, end = self.selected_data_indices[0], self.selected_data_indices[1]
            intensity_1 = self.calculate_area(self.binding_energies[start:end+1], self.intensities[start:end+1])
            
            start, end = self.selected_data_indices[2], self.selected_data_indices[3]
            intensity_2 = self.calculate_area(self.binding_energies[start:end+1], self.intensities[start:end+1])
            
            intensity_ratio = intensity_1 / intensity_2
            
            self.text_box.set_val('intensity_1 = {:.2f}; and intensity_2 = {:.2f} \nintensity_1 / intensity_2 = {:.2f}'.format(intensity_1, intensity_2, intensity_ratio))
            
            self.fig.canvas.mpl_disconnect(self.pick_event)
            self.fig.canvas.mpl_disconnect(self.key_press_event)

        
if __name__ == "__main__":
    root = Tk()
    
    Spectroscopy(root)
    
    root.mainloop()
