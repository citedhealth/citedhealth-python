# demo.tape — VHS tape for citedhealth demo GIF
# Generate with: vhs demo.tape

Output demo.gif

Set FontSize 14
Set Width 800
Set Height 400
Set Theme "Catppuccin Mocha"

Type `python3 -c "
from citedhealth import CitedHealth
client = CitedHealth()
evidence = client.get_evidence('biotin', 'hair-loss')
print(f'Grade: {evidence.grade} — {evidence.grade_label}')
print(f'Studies: {evidence.total_studies}, Participants: {evidence.total_participants}')
"`
Enter
Sleep 2s
