import sys
import logging
import pylab as plt
import os
from .interface import Interface

class DAT(Interface):
    """Read and write dat files
    
    The DAT class contains functions for reading dat files to
    a dictionary object where various calculations can be
    performed on it and then writing it back out again.
    """
    
    '''
    Constructor
    '''
    def __init__(self, datfile=None):
        ###start a log file
        self.logger = logging.getLogger('readwrite.DAT')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s',"[%Y-%m-%d %H:%M:%S]")
        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        if len(self.logger.handlers) == 0:
            self.logger.addHandler(streamhandler)
            self.logger.info('Starting a new readwrite.DAT job')        
        self.type = 'dat'
        self.is_outlier = False

        self.hashdata = {'Q': [], 'I': [], 'E': []}
        self.high_q_window_range = (0.68,0.79)
        self.low_q_window_range = (0.02,0.05)
        self.low_q_window = 0
        self.high_q_window = 0
        if self.datfile:
            self.parse_file()

    def set_datfile(self, datfile):
        '''Set the datfile'''
        if datfile == None:
            self.logger.info('No dat file provided, instantiating with empty data array')
            self.datfile = None
            return False
        elif os.path.isfile(datfile) and str(datfile)[-4:] == '.dat':
            self.datfile = str(datfile)
            self.logger.info(f'{datfile} lookks like a valid datfile')
            return True
        else:
            self.datfile = None
            self.logger.error(f'{datfile} either does not exist or is not of type ".dat"')
            return False
            
    def parse_file(self):
        self.logger.info(f'Reading and parsing dat file: {self.datfile}')
        qdata = []
        idata = []
        edata = []
        
        datafile = open(self.datfile, "r")
        saxsdata = datafile.readlines()
        for row in saxsdata:
            try:
                q = float(row.split()[0])
                i = float(row.split()[1])
                e = float(row.split()[2])
                if q > 0:
                    qdata.append(q)
                    idata.append(i)
                    edata.append(e)
            except:pass
        self.hashdata['Q'] = qdata
        self.hashdata['I'] = idata
        self.hashdata['E'] = edata

        #high Q window
        start=int(round(self.high_q_window_range[0]*len(self.ReturnDataColumn('Q'))))
        end=int(round(self.high_q_window_range[1]*len(self.ReturnDataColumn('Q'))))
        self.high_q_window = sum(self.ReturnDataColumn('I')[start:end])
        self.logger.info(f"Calculated high Q window in Q range: {self.ReturnDataColumn('Q')[start]}:{self.ReturnDataColumn('Q')[end]}")

        #low Q window
        start=int(round(self.low_q_window_range[0]*len(self.ReturnDataColumn('Q'))))
        end=int(round(self.low_q_window_range[1]*len(self.ReturnDataColumn('Q'))))
        self.low_q_window = sum(self.ReturnDataColumn('I')[start:end])
        self.logger.info('Calculated low Q window in Q range: '+str(self.ReturnDataColumn('Q')[start])+':'+str(self.ReturnDataColumn('Q')[end]))        
        self.logger.info('Parsed with '+str(len(qdata))+' data points.')

    def getHighQWindow(self):
        return self.high_q_window

    def getLowQWindow(self):
        return self.low_q_window

    def isOutlier(self, outlier=None):
        if outlier == True:
            self.is_outlier = True
            self.logger.info('Marked datfile: '+self.datfile+' as an outlier')
            return None
        elif outlier == False:
            self.is_outlier = False
            self.logger.info('Marked datfile: '+self.datfile+' as NOT an outlier')
            return None
        elif outlier == None:
            return self.is_outlier
        else:
            self.logger.error('Outlier mark should be true or false for dat class')
            return None

    def returnIEData(self, q=None):
        try:
            index = self.hashdata['Q'].index(q)
            return (self.hashdata['I'][index],self.hashdata['E'][index])
        except:
            return False

    def ReturnDataColumn(self, column='I'):
        if column in ['Q', 'I', 'E']:
            return self.hashdata[column]
        else:
            self.logger.error('ReturnDataColumn function requires you specify either Q, I or E')
            
    def return_file(self):
        self.logger.info('Writing out a formatted DAT file')
        string_list = []
        string_list.append("%-15s %-18s %-15s" % ("Q(A-1)","I(au)","Error"))
        for q in self.hashdata['Q']:
            if q > 0:
                index = self.hashdata['Q'].index(q)
                q = self.hashdata['Q'][index]
                i = self.hashdata['I'][index]
                e = self.hashdata['E'][index]
                string_list.append("%-15s %-18s %-15s" % (q,i,e))
        return '\n'.join(string_list)


    def input_dict(self, input_dict):
        self.logger.info('Reading in DAT data as a dictionary')
        if type(input_dict) == type({}):
            self.hashdata = input_dict

    def return_dict(self):
        self.logger.info('Returning DAT data as a dictionary')
        return self.hashdata

    def plot(self,
             log_y=True,
             log_x=False,
             linewidth=2,
             height=8,
             width=15,
             fontsize=16,
             title=None,
             x_label=r'Q ($\AA^{-1}$)',
             y_label=r'Intensity (cm$^{-1}$)',
             qrange_min=None,
             qrange_max=None,
             filename=None,
             label='',
             show=True
             ):
        '''Use pyplt to graph the dat data'''
        min_index = 0
        max_index = len(self.hashdata['Q'])-1
        if qrange_min:
            try:
                qrange_min = float(qrange_min)
                for i, q in enumerate(self.hashdata['Q']):
                    if q<qrange_min:
                        min_index = i
                    else:
                        break
            except:
                self.logger.error('qrange_min parameter for plot function should be a number')

        if qrange_max:
            try:
                qrange_min = float(qrange_min)
                for i, q in enumerate(self.hashdata['Q']):
                    if q>qrange_max:
                        max_index = i
                        break
            except:
                self.logger.error('1qrange_max parameter for plot function should be a number')
        if not show:
            plt.ioff()
        plt.rc('xtick',labelsize=fontsize-2)
        plt.rc('ytick',labelsize=fontsize-2)
        fig, ax = plt.subplots()
        fig.set_figwidth(width)
        fig.set_figheight(height)
        if log_y:
            plt.yscale('log')
        if log_x:
            plt.xscale('log')
        if title:
            ax.set_title(f'{title}', fontsize=fontsize)
        plt.rc('lines', linewidth=linewidth)
        ax.set_ylabel(y_label, fontsize=fontsize)
        ax.set_xlabel(x_label, fontsize=fontsize)
        plt.plot(self.hashdata['Q'][min_index:max_index],self.hashdata['I'][min_index:max_index])
        plt.title(f'{label}')
        if filename:
            plt.savefig(f'{filename}')
        if not show:
            plt.close(fig)
