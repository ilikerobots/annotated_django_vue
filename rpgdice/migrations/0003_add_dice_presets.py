from django.db import migrations

DICE_PRESETS = [
    {
        'name': 'Jump',
        'description': 'Leap, bound, or jump across non-trivial divides',
        'dice_notation': '2d8',
        'icon': 'overhead',
    },
    {
        'name': 'Fire Arrow',
        'description': 'Fire an arrow at a single target',
        'dice_notation': '2d20',
        'icon': 'arrow-flights',
    },
    {
        'name': 'Disarm Trap',
        'description': 'Attempt to disarm a trap on a door, chest, etc.',
        'dice_notation': '3d8-4',
        'icon': 'bear-trap',
    },
    {
        'name': 'Fireball',
        'description': 'The classic',
        'dice_notation': '4d12 + 10',
        'icon': 'flaming-arrow',
    },
    {
        'name': 'Dodge',
        'description': 'Get out of the way',
        'dice_notation': '3d6',
        'icon': 'player-dodge',
    },
    {
        'name': 'Repair',
        'description': 'Repair a mechanical or electronic device',
        'dice_notation': '2d10 + 4',
        'icon': 'repair',
    },
]


def add_dice_presets(apps, schema_editor):
    DicePreset = apps.get_model('rpgdice', 'DicePreset')

    for p in DICE_PRESETS:
        DicePreset.objects.get_or_create(
            name=p['name'],
            defaults={
                'description': p['description'],
                'dice_notation': p['dice_notation'],
                'icon': p['icon'],
            }
        )


def remove_dice_presets(apps, schema_editor):
    DicePreset = apps.get_model('rpgdice', 'DicePreset')
    for preset in DICE_PRESETS:
        DicePreset.objects.filter(name=preset['name']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('rpgdice', '0002_set_admin_password'),
    ]

    operations = [
        migrations.RunPython(add_dice_presets, remove_dice_presets),
    ]
