from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView

from .dice_util import roll_dice
from .models import DicePreset
from .package_info import packages


def is_ajax_request(request) -> bool:
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'package_info': packages}


class DicePresetListView(ListView):
    model = DicePreset
    template_name = 'rpgdice/dice_preset_list.html'
    context_object_name = 'dice_presets'


class RollDiceView(DetailView):
    model = DicePreset
    template_name = 'rpgdice/roll_dice_detail.html'
    context_object_name = 'preset'

    def get(self, request: object, pk: object) -> HttpResponse:
        self.object = self.get_object()

        try:
            total, dice_results, result_html = roll_dice(self.object.dice_notation)

            context = {
                'preset': self.object,
                'dice_results': dice_results,
                'result_html': result_html,
                'total_result': total,
            }

            if is_ajax_request(request):

                # django-vue: ajax-json-view@1
                # Return data, including pre-rendered result html
                return JsonResponse({
                    'total': total,
                    'is_max': all(d['value'] == d['size'] for d in dice_results),
                    'dice_results': dice_results,
                    'result_html': result_html
                })
            else:
                return self.render_to_response(context)

        except Exception as e:
            messages.error(request, f"Error rolling dice: {str(e)}", extra_tags="danger")
            return redirect('dice-preset-list')


# django-vue: render-partial-view@1
class RollKeyPartialView(TemplateView):
    template_name = 'rpgdice/dice_key.html'
