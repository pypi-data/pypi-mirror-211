# midi-clip

A python package for midi clip based on mido.

### Introduce

This library considers a lot of things for detailing midi clips: followings:

- Supports both multi-track MIDI.
- Supports both tempo track / non-tempo track
- Consider controllers that appear before start time or note_on that were not closed.
- All note_on and note_off pairs are validate. (Number of note_on and note_off is the same, and all note_ons are closed by note_off.)

### Usage

```python
import mido
import midi_clip
# load midi use mido
mid = mido.MidiFile('resources/hosu.mid')
# clip midi
output_mid = midi_clip.midi_clip(mid, 5., 15.)
# you can get total duration(second) of midi
duration = midi_clip.midi_duration(output_mid)
# if you see by print
print(output_mid, duration)
# if you save midi clip
output_mid.save('output.mid')
```

### Result

Result of clip "A Town With An Ocean View" MIDI from 0 to 30 seconds and from 5 seconds to 15 seconds.

<table>
<tr>
<td></td>
<td>Piano Roll</td>
<td>Audio</td>
</tr>
<tr>
<td>0s-30s</td>
<td><img src="./example/ocean_0_30.png"/></td>
<td></td>
</tr>
<tr>
<td>5s-15s</td>
<td><img src="./example/ocean_5_15.png"/></td>
<td></td>
</tr>
</table>

** I used GarageBand to obtain piano roll images and audio.
GarageBand fills in the measure regardless of the actual end of track time in the MIDI, resulting in slightly longer audio. MIDI file's time clip is precisely.



### Future Feature
- Currently, it clips in seconds. I'll add clips in ticks, too. MIDI default is tick, so it's easier to clip in ticks.
- (I'll add it before August)
