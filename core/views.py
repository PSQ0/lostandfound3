from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from core.models import Item
from core.forms import ItemForm
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required


def create_item(request):
    if request.method == "POST":
        form = ItemForm(
            request.POST,
            request.FILES
        )
        print(request.POST)
        print(request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(
                request,
                f"آیتم <{item.title}> با موفقیت ایجاد شد."
            )
            return redirect(
                "item_detail",
                pk=item.id
            )
        else:
            print(form.errors)
            # print("-" * 10)
            # print(form.non_field_errors())
    else:
        form = ItemForm()

    return render(
        request,
        "items/create.html",
        {"form": form}
    )


def list_items(request):
    items = Item.objects.all()
    return render(
        request,
        "items/item_list.html",
        {"items": items}
    )


def item_detail(requests, pk):
 
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=requests.user
    )

    image_size_mb = None
    if item.image:
        image_size_mb = round(item.image.size / (1024 * 1024), 2)

    return render(
        requests,
        "items/item_detail.html",
        {"item": item, "image_size_mb": image_size_mb}
    )


def update_item(request, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    if request.method == "POST":
        old_image = item.image

        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item
        )
        if form.is_valid():
            updated_item = form.save()

            if old_image and not updated_item.image:
                old_image.delete(save=False)
            messages.success(
                request,
                f"آیتم {item.title} با موفقیت ویرایش شد."
            )
            return redirect(
                "item_detail",
                pk=item.id
            )
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "items/update.html",
        {"form": form, "item": item}
    )


def delete_item(request, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    if request.method == "POST":
        item_title = item.title
        item.delete()
        messages.success(
            request,
            f"آیتم {item_title} با موفقیت حذف شد."
        )
        return redirect("list_item")

    return render(
        request,
        "items/confirm_delete.html",
        {"item": item}
    )

@login_required
def my_items(request):
    items = Item.objects.filter(created_by=request.user).order_by("-id")

    stats = items.aggregate(
        total_count=Count("id"),
        open_count=Count("id", filter=Q(status="open")),
        closed_count=Count("id", filter=Q(status="closed")),
    )

    context = {
        "items": items,
        "stats": stats,
    }
    return render(request, "items/my_items.html", context)
