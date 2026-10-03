import { routes as auth } from "../features/auth/routes";
import { routes as catalogue } from "../features/catalogue/routes";
import { routes as scheme } from "../features/scheme/routes";
import { routes as chat } from "../features/chat/routes";
import { routes as voice } from "../features/voice/routes";
import { routes as review } from "../features/review/routes";
import { routes as cases } from "../features/cases/routes";
import { routes as documents } from "../features/documents/routes";
import { routes as consent } from "../features/consent/routes";
import { routes as assisted } from "../features/assisted/routes";
import { routes as notifications } from "../features/notifications/routes";
import { routes as feedback } from "../features/feedback/routes";
import { routes as trace } from "../features/trace/routes";
import { routes as admin } from "../features/admin/routes";

export const allRoutes = [...catalogue, ...auth, ...scheme, ...chat, ...voice, ...review, ...cases, ...documents,
  ...consent, ...assisted, ...notifications, ...feedback, ...trace, ...admin];
