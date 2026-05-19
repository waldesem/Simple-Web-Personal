import { h } from "vue";
import { localStr } from "@/utils";
import { conclusions, decisions } from "@/types";
import type {
  Address,
  Affilation,
  Contact,
  Education,
  Inquisition,
  ItemField,
  Needs,
  Passport,
  Pfo,
  Previous,
  Staff,
  Verification,
  Work,
} from "@/types";

const addresses = [
  { key: "view", label: "Вид адреса" },
  { key: "address", label: "Адрес" },
] as ItemField<Address>[];

const affilations = [
  { key: "view", label: "Вид участия" },
  { key: "organization", label: "Организация" },
  { key: "inn", label: "ИНН" },
  { key: "activity", label: "Деятельность" },
] as ItemField<Affilation>[];

const checks = [
  { key: "workplace", label: "Проверка по местам работы" },
  { key: "document", label: "Проверка документов" },
  { key: "debt", label: "Проверка задолженностей" },
  { key: "bankruptcy", label: "Проверка банкротства" },
  { key: "bki", label: "Проверка Кредитной истории" },
  { key: "courts", label: "Проверка судебных дел" },
  { key: "affilation", label: "Проверка аффилированности" },
  { key: "terrorist", label: "Проверка в списке террористов" },
  { key: "internet", label: "Проверка в открытых источниках" },
  { key: "cronos", label: "Проверка в Кронос" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "comment", label: "Комментарий" },
  {
    key: "conclusion",
    label: "Результат",
    component: (row) => {
      const color =
        row.conclusion === conclusions.agreed
          ? "bg-green-500"
          : row.conclusion === conclusions.cancel
            ? "bg-gray-500"
            : row.conclusion === conclusions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return h(
        "div",
        {
          class: [
            "flex",
            "items-center",
            "inline-flex",
            "py-1 px-2",
            "rounded-md",
            "text-sm",
            "text-white",
            color,
          ],
        },
        row.conclusion,
      );
    },
  },
  { key: "created", label: "Дата записи", div: (row) => localStr(row.created) },
] as ItemField<Verification>[];

const contacts = [
  { key: "view", label: "Вид контакта" },
  { key: "contact", label: "Контакт" },
] as ItemField<Contact>[];

const documents = [
  { key: "view", label: "Вид документа" },
  { key: "series", label: "Серия документа" },
  { key: "digits", label: "Номер документа" },
  { key: "agency", label: "Кем выдан" },
  { key: "issue", label: "Дата выдачи", div: (row) => localStr(row.issue) },
] as ItemField<Passport>[];

const educations = [
  { key: "view", label: "Вид образования" },
  { key: "institution", label: "Учебное заведение" },
  { key: "finished", label: "Год окончания" },
  { key: "specialty", label: "Специальность" },
] as ItemField<Education>[];

const inquiries = [
  { key: "info", label: "Информация" },
  { key: "initiator", label: "Инициатор" },
  { key: "created", label: "Дата записи", div: (row) => localStr(row.created) },
] as ItemField<Needs>[];

const investigations = [
  { key: "theme", label: "Тема проверки" },
  { key: "info", label: "Информация" },
  { key: "created", label: "Дата записи", div: (row) => localStr(row.created) },
] as ItemField<Inquisition>[];

const poligrafs = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результат" },
  {
    key: "conclusion",
    label: "Результат",
    component: (row) => {
      const color =
        row.conclusion === decisions.agreed
          ? "bg-green-500"
          : row.conclusion === decisions.cancel
            ? "bg-gray-500"
            : row.conclusion === decisions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return () =>
        h(
          "div",
          {
            class: [
              "flex",
              "items-center",
              "inline-flex",
              "py-1 px-2",
              "rounded-md",
              "text-sm",
              "text-white",
              color,
            ],
          },
          row.conclusion,
        );
    },
  },
  { key: "created", label: "Дата записи", div: (row) => localStr(row.created) },
] as ItemField<Pfo>[];

const previous = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "changed", label: "Год изменения" },
  { key: "reason", label: "Причина" },
] as ItemField<Previous>[];

const staffs = [
  { key: "position", label: "Должность" },
  { key: "department", label: "Подразделение" },
] as ItemField<Staff>[];

const workplaces = [
  { key: "starts", label: "Начало работы", div: (row) => localStr(row.starts) },
  {
    key: "finished",
    label: "Окончание работы",
    div: (row) => localStr(row.finished),
  },
  { key: "workplace", label: "Место работы" },
  { key: "position", label: "Должность" },
  { key: "address", label: "Адрес организации" },
  { key: "reason", label: "Причина увольнения" },
] as ItemField<Work>[];

export const itemFields = {
  addresses,
  affilations,
  checks,
  contacts,
  documents,
  educations,
  inquiries,
  investigations,
  poligrafs,
  previous,
  staffs,
  workplaces,
} as { [key in keyof Items]: ItemField<Items[keyof Items]>[] };
