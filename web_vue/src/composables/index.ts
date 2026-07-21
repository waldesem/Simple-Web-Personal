import { ref } from "vue";
import type { AlertProps, ToastProps } from "@nuxt/ui";

export interface ToastComposable {
  add: (options: ToastProps) => void;
}

enum Status {
  error = "Ошибка",
  primary = "Информация",
  secondary = "Вопрос",
  success = "Успех",
  info = "Информация",
  warning = "Внимание",
  neutral = "Предупреждение",
}

enum Icons {
  error = "i-lucide-circle-x",
  primary = "i-lucide-circle-info",
  secondary = "i-lucide-circle-question-mark",
  success = "i-lucide-circle-chevron-down",
  info = "i-lucide-circle-info",
  warning = "i-lucide-circle-alert",
  neutral = "i-lucide-circle",
}

export function useToasts(toast: ToastComposable) {
  function create(
    status: ToastProps["color"] = "error",
    description: string = "Невозможно выполнить действие!",
  ) {
    toast.add({
      title: Status[status],
      description: description,
      color: status,
      icon: Icons[status],
    });
  }
  return { create };
}

export function useAlert() {
  const alert = ref<AlertProps>({
    icon: Icons.success,
    color: "success",
    title: "Вход в систему",
    description: "Введите логин и пароль.",
  });

  function update(
    status: AlertProps["color"] = "error",
    description: string = "Неизвестная ошибка.",
  ) {
    alert.value = {
      icon: Icons[status],
      color: status,
      title: Status[status],
      description: description,
    };
  }
  return { alert, update };
}
