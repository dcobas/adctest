import Generic.SineWaveform as  sw



class SineWaveform(sw.SineWaveform):
    def apply(self):
        return "APPL:SIN %f %s, %f %s, %f %s" % (self._freq[0], self._freq[1],\
                                                 self._amp[0], self._amp[1],\
                                                 self._dc[0], self._dc[1])


    
