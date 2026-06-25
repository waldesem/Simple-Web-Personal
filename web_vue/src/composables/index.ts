import { ref } from "vue";
import type { AlertProps, ToastProps } from "@nuxt/ui";

interface ToastComposable {
  add: (options: ToastProps) => void;
}

const context = {
  error: ["Ошибка", "i-mi-circle-error"],
  primary: ["Информация", "i-mi-circle-information"],
  secondary: ["Вопрос", "i-mi-circle-help"],
  success: ["Успех", "i-mi-circle-check"],
  info: ["Информация", "i-mi-circle-information"],
  warning: ["Внимание", "i-mi-circle-warning"],
  neutral: ["Предупреждение", "i-mi-circle"],
};

export function useToasts(toast: ToastComposable) {
  function create(
    status: ToastProps["color"] = "error",
    description: string = "Невозможно выполнить действие!",
  ) {
    toast.add({
      title: context[status][0],
      description: description,
      color: status,
      icon: context[status][1],
    });
  }
  return { create };
}

export function useAlert() {
  const alert = ref<AlertProps | null>(null);

  function create(
    status: AlertProps["color"] = "error",
    description: string = "Неизвестная ошибка.",
  ) {
    alert.value = {
      icon: context[status][1],
      color: status,
      title: context[status][0],
      description: description,
    };
  }
  return { alert, create };
}
