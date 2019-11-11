*****
Usage
*****

To use tiepie in a project::

   import tiepie

   # Get oscilloscope
   osc = tiepie.Oscilloscope("HS5")

   # Single shot measurement
   data = osc.measure()
