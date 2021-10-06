# ### OLD UNUSED TIMER-BASED CODE ###
#     def laser_strobe_end(self, tim_b):
#         tim_a = Timer(1)
#         tim_a.deinit()
#         self.laser_off() # make sure we end up off!

#     def laser_strobe(self, freq, duration):
#         """
#         Strobes the laser
#         freq: strobe frequency in Hz
#         duration: total active time in seconds
#         """

#         tim_a = Timer(1) # strobes the laser
#         # freq * 2 because one for on, one for off
#         tim_a.init(freq=freq*2, mode=Timer.PERIODIC, callback=lambda t: self.laser_toggle())

#         duration = int(duration * 1000)
#         tim_b = Timer(2) # turns it off
#         tim_b.init(period=duration, mode=Timer.ONE_SHOT, callback=self.laser_strobe_end)