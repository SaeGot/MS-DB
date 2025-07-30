from django.shortcuts import render, get_object_or_404
from history.models import Member, Play, PlayDate, PlayType, Participation


def search_view(request, pk=None):
    query = request.GET.get('q', '')

    members = []
    plays = []
    participations = []
    participation_map = {}
    director_map = {}
    actor_map = {}
    staff_map = {}
    selected_object = None
    selected_play_type = None
    selected_play_dates = []
    selected_type = None

    if query:
        members = Member.objects.filter(member_name__icontains=query)
        plays = Play.objects.filter(play_name__icontains=query)
        for play in plays:
            searched_play_date = PlayDate.objects.filter(play=play).order_by('play_date')[0]
            play.play_date = searched_play_date.play_date.year

    if pk and 'member' in request.path:
        selected_type = 'member'
        selected_object = get_object_or_404(Member, pk=pk)
        participations = Participation.objects.filter(member=selected_object).select_related('play', 'play_character',
                                                                                                'staff_role')

        for p in participations:
            play_date = PlayDate.objects.filter(play=p.play).order_by('play_date')[0]
            play_name = f"{p.play.play_name} ({play_date.play_date.year})"
            role_text = ""

            if p.is_staff:
                if p.staff_role:
                    role_text = f"{p.staff_role.staff_role_name}"
                else:
                    role_text = "스탭"
            else:
                if p.play_character:
                    role_text = f"배우({p.play_character.play_character_name})"
                else:
                    role_text = "배우"

            if play_name not in participation_map:
                participation_map[play_name] = []

            participation_map[play_name].append(role_text)


    elif pk and 'play' in request.path:
        selected_type = 'play'
        selected_object = get_object_or_404(Play, pk=pk)
        selected_play_type = get_object_or_404(PlayType, pk=selected_object.play_type_id)
        selected_play_dates = PlayDate.objects.filter(play=selected_object).order_by('play_date')
        participations = Participation.objects.filter(play=selected_object).select_related('member', 'play_character',
                                                                                             'staff_role')

        for p in participations:
            member_name = p.member.member_name

            if p.is_staff:
                if p.staff_role.staff_role_name=="연출" or p.staff_role.staff_role_name=="조연출":
                    staff_role_name = p.staff_role.staff_role_name
                    if staff_role_name not in director_map:
                        director_map[staff_role_name] = []
                    director_map[staff_role_name].append(member_name)
                else:
                    if p.staff_role:
                        staff_role_name = p.staff_role.staff_role_name
                    else:
                        staff_role_name = "스탭"

                    if staff_role_name not in staff_map:
                        staff_map[staff_role_name] = []
                    staff_map[staff_role_name].append(member_name)
            else:
                if p.play_character:
                    role_text = p.play_character.play_character_name
                else:
                    role_text = "배우"

                if member_name not in actor_map:
                    actor_map[member_name] = []
                actor_map[member_name].append(role_text)


    return render(request, 'search.html', {
        'query': query,
        'members': members,
        'plays': plays,
        'selected_object': selected_object,
        'selected_type': selected_type,
        'participation_map': participation_map,
        'selected_play_type': selected_play_type,
        'selected_play_dates': selected_play_dates,
        'director_map': director_map,
        'actor_map': actor_map,
        'staff_map': staff_map,
    })
